"""
Sistema de sesiones persistente para KardoCore
Usa cookies seguras con firma HMAC
"""

import hashlib
import hmac
import json
import time
from typing import Dict, Any, Optional
from pathlib import Path


class SessionManager:
    """
    Gestor de sesiones con persistencia en disco y cookies firmadas.
    """
    
    def __init__(self, secret_key: str, session_dir: str = "/tmp/kardocore_sessions"):
        """
        Inicializa el gestor de sesiones.
        
        Args:
            secret_key: Clave secreta para firmar cookies
            session_dir: Directorio para almacenar sesiones
        """
        self.secret_key = secret_key.encode()
        self.session_dir = Path(session_dir)
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self.session_lifetime = 86400  # 24 horas en segundos
    
    def create_session(self, data: Dict[str, Any]) -> str:
        """
        Crea una nueva sesión.
        
        Args:
            data: Datos a almacenar en la sesión
        
        Returns:
            ID de sesión firmado
        """
        # Generar ID único
        session_id = hashlib.sha256(
            f"{time.time()}{json.dumps(data)}".encode()
        ).hexdigest()
        
        # Agregar timestamp
        session_data = {
            "data": data,
            "created_at": time.time(),
            "expires_at": time.time() + self.session_lifetime
        }
        
        # Guardar en disco
        session_file = self.session_dir / f"{session_id}.json"
        with open(session_file, 'w') as f:
            json.dump(session_data, f)
        
        # Firmar el session ID
        signed_id = self._sign_session_id(session_id)
        
        return signed_id
    
    def get_session(self, signed_session_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene datos de una sesión.
        
        Args:
            signed_session_id: ID de sesión firmado
        
        Returns:
            Datos de la sesión o None si no existe/expiró
        """
        # Verificar firma
        session_id = self._verify_session_id(signed_session_id)
        if not session_id:
            return None
        
        # Leer del disco
        session_file = self.session_dir / f"{session_id}.json"
        if not session_file.exists():
            return None
        
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            # Verificar expiración
            if time.time() > session_data.get("expires_at", 0):
                self.destroy_session(signed_session_id)
                return None
            
            return session_data.get("data")
        except:
            return None
    
    def update_session(self, signed_session_id: str, data: Dict[str, Any]) -> bool:
        """
        Actualiza datos de una sesión.
        
        Args:
            signed_session_id: ID de sesión firmado
            data: Nuevos datos
        
        Returns:
            True si se actualizó, False si no existe
        """
        session_id = self._verify_session_id(signed_session_id)
        if not session_id:
            return False
        
        session_file = self.session_dir / f"{session_id}.json"
        if not session_file.exists():
            return False
        
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            # Actualizar datos
            session_data["data"] = data
            
            # Guardar
            with open(session_file, 'w') as f:
                json.dump(session_data, f)
            
            return True
        except:
            return False
    
    def destroy_session(self, signed_session_id: str) -> bool:
        """
        Destruye una sesión.
        
        Args:
            signed_session_id: ID de sesión firmado
        
        Returns:
            True si se destruyó, False si no existía
        """
        session_id = self._verify_session_id(signed_session_id)
        if not session_id:
            return False
        
        session_file = self.session_dir / f"{session_id}.json"
        if session_file.exists():
            session_file.unlink()
            return True
        
        return False
    
    def _sign_session_id(self, session_id: str) -> str:
        """
        Firma un session ID con HMAC.
        
        Args:
            session_id: ID de sesión sin firmar
        
        Returns:
            ID firmado en formato: session_id.signature
        """
        signature = hmac.new(
            self.secret_key,
            session_id.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return f"{session_id}.{signature}"
    
    def _verify_session_id(self, signed_session_id: str) -> Optional[str]:
        """
        Verifica la firma de un session ID.
        
        Args:
            signed_session_id: ID firmado
        
        Returns:
            ID sin firmar si es válido, None si no
        """
        try:
            session_id, signature = signed_session_id.rsplit('.', 1)
            
            # Calcular firma esperada
            expected_signature = hmac.new(
                self.secret_key,
                session_id.encode(),
                hashlib.sha256
            ).hexdigest()
            
            # Comparación segura contra timing attacks
            if hmac.compare_digest(signature, expected_signature):
                return session_id
            
            return None
        except:
            return None
    
    def cleanup_expired_sessions(self) -> int:
        """
        Limpia sesiones expiradas del disco.
        
        Returns:
            Número de sesiones eliminadas
        """
        count = 0
        current_time = time.time()
        
        for session_file in self.session_dir.glob("*.json"):
            try:
                with open(session_file, 'r') as f:
                    session_data = json.load(f)
                
                if current_time > session_data.get("expires_at", 0):
                    session_file.unlink()
                    count += 1
            except:
                # Si hay error leyendo, eliminar el archivo
                session_file.unlink()
                count += 1
        
        return count
    
    def get_cookie_header(self, signed_session_id: str, path: str = "/") -> bytes:
        """
        Genera header Set-Cookie para la sesión.
        
        Args:
            signed_session_id: ID de sesión firmado
            path: Path de la cookie
        
        Returns:
            Header Set-Cookie como bytes
        """
        cookie_value = f"kardo_session={signed_session_id}; Path={path}; HttpOnly; SameSite=Lax; Max-Age={self.session_lifetime}"
        return cookie_value.encode()
    
    def get_session_from_cookie(self, cookie_header: bytes) -> Optional[Dict[str, Any]]:
        """
        Extrae y valida sesión desde header Cookie.
        
        Args:
            cookie_header: Header Cookie como bytes
        
        Returns:
            Datos de sesión o None
        """
        try:
            cookie_str = cookie_header.decode()
            cookies = {}
            
            for cookie in cookie_str.split(';'):
                cookie = cookie.strip()
                if '=' in cookie:
                    key, value = cookie.split('=', 1)
                    cookies[key] = value
            
            session_id = cookies.get('kardo_session')
            if session_id:
                return self.get_session(session_id)
            
            return None
        except:
            return None

