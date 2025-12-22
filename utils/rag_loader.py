import os

def load_rag_data(base_path="rag_data"):
    """
    Loads text files from the rag_data directory and returns a formatted string.
    """
    rag_content = ""
    
    if not os.path.exists(base_path):
        return "Error: rag_data directory not found."

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        # Create a header based on the directory and filename
                        relative_path = os.path.relpath(file_path, base_path)
                        rag_content += f"\n--- DOCUMENT START: {relative_path} ---\n"
                        rag_content += content
                        rag_content += f"\n--- DOCUMENT END: {relative_path} ---\n"
                except Exception as e:
                    rag_content += f"\nError reading file {file}: {str(e)}\n"
    
    return rag_content
