import argparse
import sys
import os

from core.lang.nor import NoR;

def main():
    parser = argparse.ArgumentParser(description="NoR언어 인터프리터")
    parser.add_argument("script_file", help="실행할 .nor 스크립트 파일의 경로입니다.")
    parser.add_argument("--debug", action="store_true", help="인터프리터의 디버그 모드를 활성화합니다.")

    args = parser.parse_args()

    try:
        with open(args.script_file, 'r', encoding='utf-8') as f:
            script_content = f.read()
    except FileNotFoundError:
        print(f"오류: 스크립트 파일 '{args.script_file}'을(를) 찾을 수 없습니다.", file=sys.stderr)
        sys.exit(1) 
    except Exception as e:
        print(f"스크립트 파일 '{args.script_file}' 읽기 오류: {e}", file=sys.stderr)
        sys.exit(1)

    nor_interpreter = NoR(debug_mode=args.debug, server_mode=False)

    results = nor_interpreter.run(script_content)

    if results:
        for item in results:
            print(item)

    had_errors = False
    if hasattr(nor_interpreter, 'logs') and isinstance(nor_interpreter.logs, list):
        if any(log.type == "error" for log in nor_interpreter.logs if hasattr(log, 'type')):
            had_errors = True
    
    if had_errors:
        sys.exit(1) 
    else:
        sys.exit(0) 

if __name__ == "__main__":
    main()