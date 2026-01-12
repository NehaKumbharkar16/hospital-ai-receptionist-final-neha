Title: Fix syntax error in test_deployment.py

Summary:
- Fixes a SyntaxError in `test_deployment.py` where a malformed print statement caused pytest collection to fail.
- Also resolves a merge conflict in `vercel.json` and updates it to a minimal Vercel config.

Details:
- `test_deployment.py`: corrected a broken print statement to properly log the chat API response.
- `vercel.json`: resolved merge conflict and ensured a valid Vercel configuration for the frontend.

Verification:
- Ran test suite: `pytest -q` — all tests pass (10 passed).
- Started the backend server and confirmed it responds at `http://127.0.0.1:8000`.
- Started the frontend dev server and confirmed UI is available at `http://localhost:5174/`.

Notes:
- No Supabase or Google API credentials were set in this environment (non-blocking warnings during startup).
- If you want, I can add reviewers/assignees; tell me who to add and I'll include them in the PR description or push a follow-up commit.

Suggested PR body:
This PR fixes a SyntaxError discovered during `pytest` collection and resolves a small merge conflict in `vercel.json`.
All tests now pass and both frontend and backend were smoke-tested locally.

---

(Automated note: PR branch: `fix/test-deployment`)
