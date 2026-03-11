#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Feishu Markdown Uploader with Ownership Transfer
将本地 Markdown 文件上传到飞书并转移所有权
"""

import urllib.request
import json
import time
import os
import sys
import codecs
from typing import Dict, Optional, Tuple

# 设置输出编码
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

class FeishuUploader:
    """飞书 Markdown 上传器 - 支持所有权转移"""
    
    BASE_URL = "https://open.feishu.cn/open-apis"
    
    def __init__(self, app_id: str, app_secret: str, owner_user_id: Optional[str] = None):
        """
        初始化上传器
        
        Args:
            app_id: 飞书应用 ID
            app_secret: 飞书应用密钥
            owner_user_id: 目标所有者用户 ID (可选)
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.owner_user_id = owner_user_id  # 用户 ID (如 G5474)
        self.owner_open_id = None  # 用户的 open_id
        self.token = None
        
    def log(self, message: str):
        """输出日志"""
        try:
            print(message)
        except:
            print(message.encode('ascii', 'ignore').decode())
        
    def get_tenant_access_token(self) -> Optional[str]:
        """获取 Tenant Access Token"""
        url = f"{self.BASE_URL}/auth/v3/tenant_access_token/internal"
        data = json.dumps({
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }).encode('utf-8')
        
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"}
        )
        
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode())
                if result.get("code") == 0:
                    self.token = result["tenant_access_token"]
                    return self.token
                else:
                    self.log(f"[ERROR] 获取 Token 失败: {result}")
                    return None
        except Exception as e:
            self.log(f"[ERROR] 获取 Token 出错: {e}")
            return None
    
    def get_user_open_id(self) -> Optional[str]:
        """通过 user_id 获取 open_id"""
        if not self.token or not self.owner_user_id:
            return None
        
        # 尝试从 user_id 获取 open_id
        # 注意：这里可能需要 contact:user.base:readonly 权限
        url = f"{self.BASE_URL}/contact/v3/users/{self.owner_user_id}"
        req = urllib.request.Request(
            url,
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode())
                if result.get("code") == 0:
                    self.owner_open_id = result["data"]["user"]["open_id"]
                    self.log(f"[OK] 获取用户 open_id: {self.owner_open_id}")
                    return self.owner_open_id
        except Exception as e:
            self.log(f"[WARN] 获取用户 open_id 失败: {e}")
        
        # 如果失败，尝试使用用户ID作为open_id
        self.owner_open_id = self.owner_user_id
        return self.owner_open_id
    
    def upload_file(self, file_path: str, folder_token: str) -> Optional[str]:
        """上传文件到飞书 Drive"""
        if not self.token:
            self.log("[ERROR] Token 未获取")
            return None
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        filename = os.path.basename(file_path)
        boundary = "----7MA4YWxkTrZu0gW"
        
        # 构建 multipart body
        body_parts = [
            f"--{boundary}",
            'Content-Disposition: form-data; name="file_name"',
            "",
            filename,
            f"--{boundary}",
            'Content-Disposition: form-data; name="parent_type"',
            "",
            "ccm_import_open",
            f"--{boundary}",
            'Content-Disposition: form-data; name="size"',
            "",
            str(len(content.encode('utf-8'))),
            f"--{boundary}",
            'Content-Disposition: form-data; name="extra"',
            "",
            '{"obj_type":"docx","file_extension":"md"}',
            f"--{boundary}",
            f'Content-Disposition: form-data; name="file"; filename="{filename}"',
            "Content-Type: text/markdown",
            "",
            content,
            f"--{boundary}--"
        ]
        
        body_str = "\r\n".join(body_parts)
        body_bytes = body_str.encode('utf-8')
        
        url = f"{self.BASE_URL}/drive/v1/medias/upload_all"
        req = urllib.request.Request(
            url,
            data=body_bytes,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": f"multipart/form-data; boundary={boundary}"
            }
        )
        
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode())
                if result.get("code") == 0:
                    file_token = result["data"]["file_token"]
                    self.log(f"[OK] 文件上传成功: {file_token}")
                    return file_token
                else:
                    self.log(f"[ERROR] 上传失败: {result}")
                    return None
        except Exception as e:
            self.log(f"[ERROR] 上传出错: {e}")
            return None
    
    def create_import_task(self, file_token: str, folder_token: str, title: str) -> Optional[str]:
        """创建导入任务 (md -> docx)"""
        if not self.token:
            return None
        
        url = f"{self.BASE_URL}/drive/v1/import_tasks"
        data = json.dumps({
            "file_extension": "md",
            "file_token": file_token,
            "type": "docx",
            "file_name": title,
            "point": {
                "mount_type": 1,
                "mount_key": folder_token
            }
        }).encode('utf-8')
        
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
        )
        
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode())
                if result.get("code") == 0:
                    ticket = result["data"]["ticket"]
                    self.log(f"[OK] 导入任务创建成功: {ticket}")
                    return ticket
                else:
                    self.log(f"[ERROR] 创建导入任务失败: {result}")
                    return None
        except Exception as e:
            self.log(f"[ERROR] 创建导入任务出错: {e}")
            return None
    
    def check_import_status(self, ticket: str) -> Tuple[bool, Optional[str]]:
        """检查导入状态"""
        if not self.token:
            return False, None
        
        url = f"{self.BASE_URL}/drive/v1/import_tasks/{ticket}"
        req = urllib.request.Request(
            url,
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode())
                if result.get("code") == 0:
                    status = result["data"]["result"]["job_status"]
                    if status == 0:
                        doc_token = result["data"]["result"].get("token")
                        return True, doc_token
                    elif status in [2, 3]:
                        self.log(f"[ERROR] 导入失败/超时: status={status}")
                        return False, None
                    else:
                        return False, None
                else:
                    self.log(f"[ERROR] 检查状态失败: {result}")
                    return False, None
        except Exception as e:
            self.log(f"[ERROR] 检查状态出错: {e}")
            return False, None
    
    def transfer_ownership(self, doc_token: str) -> bool:
        """
        转移文档所有权给指定用户
        
        注意：飞书 API 限制，租户 token 创建的文档无法直接转移所有权
        替代方案：添加用户为协作者并赋予 full_access 权限
        """
        if not self.token or not self.owner_user_id:
            self.log("[WARN] 未提供目标用户ID，跳过所有权转移")
            return False
        
        self.log("[STEP 5] 尝试转移所有权...")
        
        # 获取用户的 open_id
        if not self.get_user_open_id():
            self.log("[WARN] 无法获取用户 open_id，尝试使用提供的 user_id")
            self.owner_open_id = self.owner_user_id
        
        # 方法1: 尝试添加协作者（赋予完全权限）
        success = self._add_collaborator(doc_token)
        if success:
            self.log("[OK] 已添加用户为协作者（完全权限）")
            return True
        
        # 方法2: 尝试设置公开权限
        self._set_public_permission(doc_token)
        
        return False
    
    def _add_collaborator(self, doc_token: str) -> bool:
        """添加协作者"""
        # 尝试多个可能的 API 端点
        endpoints = [
            # Drive V1 成员管理
            (f"{self.BASE_URL}/drive/v1/files/{doc_token}/members", {
                "members": [{
                    "member_type": "openid",
                    "member_id": self.owner_open_id,
                    "perm": "full_access"
                }]
            }),
            # Docx 协作者
            (f"{self.BASE_URL}/docx/v1/documents/{doc_token}/collaborators", {
                "collaborators": [{
                    "member_type": "openid",
                    "member_id": self.owner_open_id,
                    "perm": "full_access"
                }]
            }),
        ]
        
        for url, data in endpoints:
            try:
                req = urllib.request.Request(
                    url,
                    data=json.dumps(data).encode(),
                    headers={
                        "Authorization": f"Bearer {self.token}",
                        "Content-Type": "application/json"
                    },
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    result = json.loads(resp.read().decode())
                    if result.get("code") == 0:
                        return True
            except:
                continue
        
        return False
    
    def _set_public_permission(self, doc_token: str) -> bool:
        """设置公开权限"""
        urls = [
            f"{self.BASE_URL}/drive/v1/permissions/{doc_token}/public",
            f"{self.BASE_URL}/drive/v2/permission/{doc_token}/public",
        ]
        
        data = {
            "link_share_entity": "tenant_readable",
            "external_access_entity": "block",
            "copy_entity": "anyone",
            "share_entity": "anyone"
        }
        
        for url in urls:
            try:
                req = urllib.request.Request(
                    url,
                    data=json.dumps(data).encode(),
                    headers={
                        "Authorization": f"Bearer {self.token}",
                        "Content-Type": "application/json"
                    },
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    result = json.loads(resp.read().decode())
                    if result.get("code") == 0:
                        self.log("[OK] 已设置公开权限")
                        return True
            except:
                continue
        
        return False
    
    def upload_md_to_feishu(self, file_path: str, folder_token: str, 
                           title: Optional[str] = None) -> Dict:
        """
        上传 MD 文件到飞书并转移所有权
        
        Args:
            file_path: 本地 MD 文件路径
            folder_token: 目标文件夹 token
            title: 文档标题（可选）
        
        Returns:
            {"success": bool, "url": str, "document_token": str, "title": str, "ownership_transferred": bool}
        """
        start_time = time.time()
        
        # 1. 获取 Token
        self.log("[STEP 1] 获取访问令牌...")
        if not self.get_tenant_access_token():
            return {"success": False, "error": "获取 Token 失败"}
        
        # 2. 上传文件
        self.log(f"[STEP 2] 上传文件: {file_path}")
        file_token = self.upload_file(file_path, folder_token)
        if not file_token:
            return {"success": False, "error": "文件上传失败"}
        
        # 3. 创建导入任务
        doc_title = title or os.path.basename(file_path).replace(".md", "")
        self.log(f"[STEP 3] 创建导入任务: {doc_title}")
        ticket = self.create_import_task(file_token, folder_token, doc_title)
        if not ticket:
            return {"success": False, "error": "创建导入任务失败"}
        
        # 4. 等待导入完成
        self.log("[STEP 4] 等待导入完成...")
        doc_token = None
        for i in range(20):  # 最多等待 40 秒
            time.sleep(1)  # 减少等待时间
            success, doc_token = self.check_import_status(ticket)
            if success and doc_token:
                break
            self.log(f"  检查 {i+1}/20: 转换中...")
        
        if not doc_token:
            return {"success": False, "error": "导入超时或失败"}
        
        url = f"https://feishu.cn/docx/{doc_token}"
        self.log(f"[OK] 导入成功!")
        self.log(f"[URL] {url}")
        
        # 5. 转移所有权（如提供了用户ID）
        ownership_transferred = False
        if self.owner_user_id:
            ownership_transferred = self.transfer_ownership(doc_token)
        
        elapsed = time.time() - start_time
        self.log(f"[TIME] 总耗时: {elapsed:.2f} 秒")
        
        return {
            "success": True,
            "url": url,
            "document_token": doc_token,
            "title": doc_title,
            "ownership_transferred": ownership_transferred
        }


def main():
    """命令行入口"""
    if len(sys.argv) < 5:
        print("用法: python feishu_uploader.py <app_id> <app_secret> <folder_token> <file_path> [title] [user_id]")
        print("  user_id: 可选，目标所有者用户ID（如 G5474）")
        sys.exit(1)
    
    app_id = sys.argv[1]
    app_secret = sys.argv[2]
    folder_token = sys.argv[3]
    file_path = sys.argv[4]
    title = sys.argv[5] if len(sys.argv) > 5 else None
    user_id = sys.argv[6] if len(sys.argv) > 6 else None
    
    uploader = FeishuUploader(app_id, app_secret, user_id)
    result = uploader.upload_md_to_feishu(file_path, folder_token, title)
    
    if result["success"]:
        print(f"\n[DONE] 完成!")
        print(f"  URL: {result['url']}")
        print(f"  所有权转移: {'成功' if result.get('ownership_transferred') else '未完成'}")
        print(f"[JSON] {json.dumps(result, ensure_ascii=False)}")
    else:
        print(f"\n[FAILED] 失败: {result.get('error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
