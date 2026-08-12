import subprocess
import json
import sys

def test_stdio():
    # Start server.py as a subprocess
    cmd = [sys.executable, "server.py"]
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=r"C:\Users\SRIKARREDDY\.gemini\antigravity\scratch\VTU25754"
    )

    # Send initialize JSON-RPC request
    init_req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0.0"}
        }
    }
    
    proc.stdin.write(json.dumps(init_req) + "\n")
    proc.stdin.flush()

    response = proc.stdout.readline()
    print("Initialize Response:", response)

    # Send tools/list request
    list_req = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    proc.stdin.write(json.dumps(list_req) + "\n")
    proc.stdin.flush()

    response = proc.stdout.readline()
    print("Tools List Response:", response)

    # Send tools/call request
    call_req = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "write_and_save_story",
            "arguments": {
                "topic": "A secret doorway in a library",
                "filename": "bionic_test.txt",
                "genre": "mystery"
            }
        }
    }
    proc.stdin.write(json.dumps(call_req) + "\n")
    proc.stdin.flush()

    response = proc.stdout.readline()
    print("Tools Call Response:", response)

    proc.terminate()

if __name__ == "__main__":
    test_stdio()
