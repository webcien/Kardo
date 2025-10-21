#!/usr/bin/env python3
"""
Script de prueba para compilar KardoCSS

Genera un archivo CSS completo para verificar que el compilador funciona.
"""

import sys
from pathlib import Path

# Agregar el directorio al path
sys.path.insert(0, str(Path(__file__).parent))

from kardocss import KardoCSSConfig, KardoCSSCompiler


def main():
    print("\n" + "="*60)
    print("  KardoCSS - Test de Compilación")
    print("="*60 + "\n")
    
    # Crear configuración
    print("📝 Creando configuración...")
    config = KardoCSSConfig()
    
    # Crear compilador
    print("🔨 Inicializando compilador...")
    compiler = KardoCSSCompiler(config)
    
    # Compilar CSS
    print("⚙️  Compilando CSS...")
    
    # CSS normal
    css = compiler.compile(minify=False)
    output_path = Path(__file__).parent / "dist" / "kardocss.css"
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(css)
    
    print(f"✅ CSS compilado: {output_path}")
    print(f"📏 Tamaño: {len(css)} bytes ({len(css) / 1024:.2f} KB)")
    
    # CSS minificado
    print("\n⚙️  Compilando CSS minificado...")
    css_min = compiler.compile(minify=True)
    output_path_min = Path(__file__).parent / "dist" / "kardocss.min.css"
    
    with open(output_path_min, 'w', encoding='utf-8') as f:
        f.write(css_min)
    
    print(f"✅ CSS minificado: {output_path_min}")
    print(f"📏 Tamaño: {len(css_min)} bytes ({len(css_min) / 1024:.2f} KB)")
    
    # Estadísticas
    reduction = ((len(css) - len(css_min)) / len(css)) * 100
    print(f"\n📊 Reducción: {reduction:.1f}%")
    
    print("\n" + "="*60)
    print("✨ Compilación completada exitosamente")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()

