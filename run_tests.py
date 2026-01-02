#!/usr/bin/env python3
"""Script para executar todos os testes do projeto.

Este script executa todos os testes de design patterns de forma sequencial.
Funciona tanto dentro do container Docker quanto localmente.
"""

import sys
import subprocess
import os
from pathlib import Path

# Cores para output (compatível com Windows)
if os.name == 'nt' or not sys.stdout.isatty():  # Windows ou não é terminal
    GREEN = RED = YELLOW = RESET = BOLD = ""
    CHECK = "[OK]"
    CROSS = "[X]"
else:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CHECK = "[OK]"
    CROSS = "[X]"

def run_test(test_path: Path) -> bool:
    """Executa um teste e retorna True se passou."""
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}Executando: {test_path.name}{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")
    
    try:
        result = subprocess.run(
            [sys.executable, str(test_path)],
            cwd=test_path.parent.parent.parent,
            check=True,
            capture_output=False
        )
        print(f"\n{GREEN}{CHECK} {test_path.name} - PASSOU{RESET}\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n{RED}{CROSS} {test_path.name} - FALHOU (código: {e.returncode}){RESET}\n")
        return False
    except Exception as e:
        print(f"\n{RED}{CROSS} {test_path.name} - ERRO: {e}{RESET}\n")
        return False


def main():
    """Executa todos os testes do projeto."""
    base_dir = Path(__file__).parent / "src"
    
    # Lista de todos os testes
    test_files = [
        base_dir / "behavioral" / "state" / "test_state.py",
        base_dir / "behavioral" / "strategy" / "test_strategy.py",
        base_dir / "behavioral" / "template_method" / "test_template_method.py",
        base_dir / "behavioral" / "observer" / "test_observer.py",
        base_dir / "structural" / "adapter" / "test_adapter.py",
        base_dir / "structural" / "decorator" / "test_decorator.py",
        base_dir / "structural" / "facade" / "test_facade.py",
    ]
    
    # Verificar quais testes existem
    existing_tests = [t for t in test_files if t.exists()]
    
    if not existing_tests:
        print(f"{RED}Nenhum teste encontrado!{RESET}")
        return 1
    
    print(f"\n{BOLD}{YELLOW}Executando {len(existing_tests)} arquivos de teste...{RESET}\n")
    
    results = []
    for test_file in existing_tests:
        success = run_test(test_file)
        results.append((test_file.name, success))
    
    # Resumo final
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}RESUMO DOS TESTES{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")
    
    passed = sum(1 for _, success in results if success)
    failed = len(results) - passed
    
    for name, success in results:
        status = f"{GREEN}{CHECK} PASSOU{RESET}" if success else f"{RED}{CROSS} FALHOU{RESET}"
        print(f"  {name}: {status}")
    
    print(f"\n{BOLD}Total: {len(results)} testes | {GREEN}Passou: {passed}{RESET} | {RED}Falhou: {failed}{RESET}\n")
    
    if failed > 0:
        print(f"{RED}{BOLD}Alguns testes falharam!{RESET}\n")
        return 1
    else:
        print(f"{GREEN}{BOLD}Todos os testes passaram! {CHECK}{RESET}\n")
        return 0


if __name__ == "__main__":
    sys.exit(main())

