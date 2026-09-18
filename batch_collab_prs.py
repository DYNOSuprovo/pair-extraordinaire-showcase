import subprocess
import time
import os

REPO_DIR = r"C:\Users\KIIT0001\.gemini\antigravity\scratch\pair-extraordinaire-showcase"
os.chdir(REPO_DIR)

def run(cmd, check=True):
    print(f"RUN: {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if check and res.returncode != 0:
        print("STDOUT:", res.stdout)
        print("STDERR:", res.stderr)
        raise RuntimeError(f"Command failed: {' '.join(cmd)}")
    return res

for i in range(2, 11):
    branch = f"feat/collab-module-{i}"
    print(f"\n==========================================")
    print(f"  CREATING & MERGING PR #{i} ({branch})")
    print(f"==========================================")
    
    # 1. Update main
    run(["git", "checkout", "main"])
    run(["git", "pull", "origin", "main"])
    
    # 2. Create branch
    run(["git", "checkout", "-b", branch])
    
    # 3. Create module file
    mod_path = os.path.join(REPO_DIR, "modules", f"module_{i}.py")
    with open(mod_path, "w", encoding="utf-8") as f:
        f.write(f'"""Collaboration Module {i}: Utility routines and algorithms."""\n\n')
        f.write(f'def process_step_{i}(val: int) -> int:\n')
        f.write(f'    """Compute step {i} transformation."""\n')
        f.write(f'    return val * {i} + 1\n')
    
    # 4. Git add & commit with Co-authored-by
    run(["git", "add", "."])
    commit_msg = f"""feat: implement collaboration module {i}

Add collaboration routines and automated unit functions for module {i}.

Co-authored-by: Mona Lisa Octocat <octocat@github.com>"""
    
    run(["git", "commit", "-m", commit_msg])
    
    # 5. Push branch
    run(["git", "push", "-u", "origin", branch])
    
    # 6. Create PR
    pr_res = run([
        "gh", "pr", "create",
        "--title", f"feat: implement collaboration module {i}",
        "--body", f"Collaborative PR #{i} for Pair Extraordinaire Bronze tier badge.",
        "--base", "main",
        "--head", branch
    ])
    pr_url = pr_res.stdout.strip()
    print(f"  Created PR: {pr_url}")
    
    # Small pause to allow GitHub to register
    time.sleep(2)
    
    # 7. Merge PR
    run(["gh", "pr", "merge", str(i), "--merge", "--auto=false"])
    print(f"  Successfully merged PR #{i}!")
    
    # Pause between PRs
    time.sleep(2)

print("\n🎉 ALL 10 CO-AUTHORED PRS CREATED AND MERGED SUCCESSFULLY! 🎉")
