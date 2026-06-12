"""Servicios del motor de análisis.

Proporciona `analyze_code` para analizar Java, C# y Python.
Para Java usa AST con javalang; para C#/Python usa estimaciones
basadas en expresiones regulares.
"""
from __future__ import annotations

import ast
import re
from typing import Any, Dict, List

import javalang


def analyze_code(code_string: str, extension: str) -> Dict[str, Any]:
    """Analiza código fuente (Java, C# o Python) y devuelve métricas homogéneas."""
    # Contar LOC (líneas no vacías)
    loc = sum(1 for line in code_string.splitlines() if line.strip())

    complexity = 0
    code_smells: List[str] = []
    # métricas estructurales nuevas
    nom = 0  # Number of Methods (NOM)
    npm = 0  # Number of Public Methods (NPM)
    noa = 0  # Number of Attributes (NOA)
    method_count = 0
    cloc = 0
    ext = (extension or "").lower()

    if ext == ".java":
        # Lógica Java intacta: AST con javalang + code smells actuales.
        try:
            cu = javalang.parse.parse(code_string)

            # contar estructuras de control
            for _, node in cu.filter(javalang.tree.IfStatement):
                complexity += 1
            for _, node in cu.filter(javalang.tree.ForStatement):
                complexity += 1
            for _, node in cu.filter(javalang.tree.WhileStatement):
                complexity += 1
            for _, node in cu.filter(javalang.tree.SwitchStatement):
                complexity += 1
            for _, node in cu.filter(javalang.tree.CatchClause):
                complexity += 1
            # contar declaraciones de método y detectar parámetros largos
            for _, node in cu.filter(javalang.tree.MethodDeclaration):
                method_count += 1
                nom += 1
                params = getattr(node, "parameters", []) or []
                modifiers = getattr(node, "modifiers", []) or []
                if "public" in modifiers:
                    npm += 1
                if len(params) > 5:
                    name = getattr(node, "name", "<anonymous>")
                    code_smells.append(f"Long Parameter List en método: {name}")
            # contar declaraciones de campos/atributos
            for _, node in cu.filter(javalang.tree.FieldDeclaration):
                noa += 1
        except javalang.parser.JavaSyntaxError:
            # Si falla el parse, usar conteo simple por palabras clave como fallback
            lowered = f" {code_string.lower()} "
            complexity = (
                lowered.count(" if ")
                + lowered.count(" for ")
                + lowered.count(" while ")
                + lowered.count(" switch ")
                + lowered.count(" catch ")
            )
            # no podemos obtener AST, dejar métricas estructurales a cero
            nom = 0
            npm = 0
            noa = 0

        # Detectar métodos largos (>50 LOC) mediante regex y balanceo de llaves
        method_pattern = re.compile(
            r'(?:(?:public|protected|private|static|final|synchronized|abstract|native|strictfp)\s+)*'
            r'(?:[\w\<\>\[\]]+\s+)?'  # tipo de retorno opcional (constructor permitido)
            r'(?P<name>[A-Za-z_][\w]*)\s*\([^)]*\)\s*\{',
            re.MULTILINE,
        )

        for m in method_pattern.finditer(code_string):
            name = m.group("name")
            idx = m.end()
            brace_count = 1
            i = idx
            length = len(code_string)
            while i < length and brace_count > 0:
                ch = code_string[i]
                if ch == "{":
                    brace_count += 1
                elif ch == "}":
                    brace_count -= 1
                i += 1

            method_body = code_string[m.start():i]
            method_loc = sum(1 for line in method_body.splitlines() if line.strip())
            if method_loc > 50:
                code_smells.append(f"Long method: {name} ({method_loc} LOC)")

    elif ext in [".cs", ".py"]:
        lowered = f" {code_string.lower()} "

        # Complejidad estimada por regex (incluye elif para Python)
        complexity_keywords = ["if", "for", "while", "switch", "elif", "catch"]
        for kw in complexity_keywords:
            complexity += len(re.findall(rf"\b{re.escape(kw)}\b", lowered))

        if ext == ".py":
            try:
                tree = ast.parse(code_string)
                nom_ast = 0
                npm_ast = 0
                noa_ast = 0
                
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        nom_ast += 1
                        if not node.name.startswith("_"):
                            npm_ast += 1
                        
                        # Code Smell: Long Parameter List
                        # Calculate total parameters
                        num_params = len(node.args.args) + len(node.args.kwonlyargs)
                        if hasattr(node.args, 'posonlyargs'):
                            num_params += len(node.args.posonlyargs)
                        if node.args.vararg: num_params += 1
                        if node.args.kwarg: num_params += 1
                        
                        if num_params > 5:
                            code_smells.append(f"Long Parameter List en método: {node.name}")
                            
                        # Code Smell: Long Method
                        if hasattr(node, "end_lineno") and node.end_lineno is not None:
                            method_loc = node.end_lineno - node.lineno + 1
                            if method_loc > 50:
                                code_smells.append(f"Long method: {node.name} ({method_loc} LOC)")
                    
                    elif isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == "self":
                                noa_ast += 1
                                
                nom = nom_ast
                method_count = nom
                npm = npm_ast
                noa = noa_ast
            except SyntaxError:
                # Fallback to simple regex if syntax error
                def_matches = re.findall(r"^\s*def\s+([A-Za-z_][\w]*)\s*\(", code_string, re.MULTILINE)
                nom = len(def_matches)
                method_count = nom
                npm = sum(1 for name in def_matches if not name.startswith("_"))
                noa = len(re.findall(r"\bself\.([A-Za-z_][\w]*)\s*=", code_string))
                
                for m in re.finditer(r"^(?P<indent>[ \t]*)def\s+(?P<name>[A-Za-z_][\w]*)\s*\((?P<params>[^)]*)\):", code_string, re.MULTILINE):
                    indent = m.group("indent")
                    name = m.group("name")
                    params_str = m.group("params")
                    params_list = [p for p in params_str.split(",") if p.strip() and p.strip() != "self"]
                    if len(params_list) > 5:
                        code_smells.append(f"Long Parameter List en método: {name}")

                    # method loc
                    start_idx = m.end()
                    method_body = code_string[start_idx:]
                    method_loc = m.group(0).count('\n') + 1
                    for line in method_body.splitlines():
                        if not line.strip():
                            method_loc += 1
                        elif line.startswith(indent + " ") or line.startswith(indent + "\t"):
                            method_loc += 1
                        else:
                            if not line.strip().startswith("#"):
                                break
                            method_loc += 1
                            
                    if method_loc > 50:
                        code_smells.append(f"Long method: {name} ({method_loc} LOC)")

            # CLOC: `#` por línea + docstrings multilinea
            cloc += sum(1 for line in code_string.splitlines() if re.search(r"(^|\s)#", line))
            for match in re.findall(r'""".*?"""|\'\'\'.*?\'\'\'', code_string, re.DOTALL):
                cloc += match.count("\n") + 1
        else:
            # C#
            method_matches = re.findall(
                r"\b(public|protected|private|internal)\s+(?:static\s+)?(?:async\s+)?[\w<>,\[\]\?]+\s+([A-Za-z_][\w]*)\s*\(",
                code_string,
            )
            nom = len(method_matches)
            method_count = nom
            npm = sum(1 for visibility, _ in method_matches if visibility == "public")
            # NOA: campos simples en clase
            field_matches = re.findall(
                r"^\s*(?:public|protected|private|internal)\s+(?:static\s+)?[\w<>,\[\]\?]+\s+[A-Za-z_][\w]*\s*(?:=|;)",
                code_string,
                re.MULTILINE,
            )
            noa = len(field_matches)
            
            # Detect smells in C#
            cs_method_pattern = re.compile(
                r'(?:(?:public|protected|private|internal|static|virtual|override|sealed|async|new|readonly)\s+)*'
                r'(?:[\w\<\>\[\]\?]+\s+)?'
                r'(?P<name>[A-Za-z_][\w]*)\s*\((?P<params>[^)]*)\)[^{;]*\{',
                re.MULTILINE,
            )
            for m in cs_method_pattern.finditer(code_string):
                name = m.group("name")
                if name in ["if", "for", "while", "catch", "switch", "using", "lock", "foreach"]:
                    continue
                    
                params_str = m.group("params")
                params_list = [p for p in params_str.split(",") if p.strip()]
                if len(params_list) > 5:
                    code_smells.append(f"Long Parameter List en método: {name}")

                idx = m.end() - 1
                brace_count = 1
                i = idx + 1
                length = len(code_string)
                while i < length and brace_count > 0:
                    ch = code_string[i]
                    if ch == "{":
                        brace_count += 1
                    elif ch == "}":
                        brace_count -= 1
                    i += 1

                method_body = code_string[idx:i]
                method_loc = sum(1 for line in method_body.splitlines() if line.strip())
                if method_loc > 50:
                    code_smells.append(f"Long method: {name} ({method_loc} LOC)")
            
            # CLOC estilo C/C#
            for match in re.findall(r"/\*.*?\*/", code_string, re.DOTALL):
                cloc += match.count("\n") + 1
            cloc += sum(1 for line in code_string.splitlines() if "//" in line)

    else:
        # Extensión no soportada específicamente: fallback genérico.
        lowered = f" {code_string.lower()} "
        complexity_keywords = ["if", "for", "while", "switch", "elif", "catch", "match", "case"]
        for kw in complexity_keywords:
            complexity += len(re.findall(rf"\b{re.escape(kw)}\b", lowered))
            
        cloc += sum(1 for line in code_string.splitlines() if "//" in line or "#" in line)
        for match in re.findall(r"/\*.*?\*/", code_string, re.DOTALL):
            cloc += match.count("\n") + 1

        # Heurística genérica para detectar métodos/funciones
        generic_method_pattern = re.compile(
            r'(?:(?:public|protected|private|static|export|default|async|function|func)\s+)*'
            r'(?:[\w\<\>\[\]\?\*]+\s+)?'
            r'(?P<name>[A-Za-z_][\w]*)\s*\((?P<params>[^)]*)\)\s*(?::\s*[\w\<\>\[\]\?]+\s*)?\{',
            re.MULTILINE
        )
        
        for m in generic_method_pattern.finditer(code_string):
            name = m.group("name")
            
            # Evitar falsos positivos como palabras reservadas de control
            if name in ["if", "for", "while", "switch", "catch", "function", "func", "else", "elseif"]:
                continue
                
            nom += 1
            method_count += 1
            npm += 1 

            params_str = m.group("params")
            params_list = [p for p in params_str.split(",") if p.strip()]
            if len(params_list) > 5:
                code_smells.append(f"Long Parameter List en método: {name}")

            idx = m.end() - 1
            brace_count = 1
            i = idx + 1
            length = len(code_string)
            while i < length and brace_count > 0:
                ch = code_string[i]
                if ch == "{":
                    brace_count += 1
                elif ch == "}":
                    brace_count -= 1
                i += 1

            method_body = code_string[idx:i]
            method_loc = sum(1 for line in method_body.splitlines() if line.strip())
            if method_loc > 50:
                code_smells.append(f"Long method: {name} ({method_loc} LOC)")

    # CLOC para Java (fuera de rama por compatibilidad con lógica previa)
    if ext == ".java":
        for match in re.findall(r"/\*.*?\*/", code_string, re.DOTALL):
            cloc += match.count("\n") + 1
        cloc += sum(1 for line in code_string.splitlines() if "//" in line)

    return {
        "loc": loc,
        "complexity": complexity,
        "method_count": method_count,
        "nom": nom,
        "npm": npm,
        "noa": noa,
        "cloc": cloc,
        "code_smells": code_smells,
    }
