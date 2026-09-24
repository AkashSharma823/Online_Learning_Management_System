# Heartify LMS — Error Audit and Fix Report

## Defects identified and fixed

1. **Broken nested dashboard routing** — role routes were declared with absolute child paths inside a nested `Routes` tree. The children now use relative paths (`dashboard`, `courses`, etc.), so `/student/*`, `/instructor/*`, and `/admin/*` resolve correctly.
2. **Instructor/admin profile links could lead to the public 404 redirect** — only the student role had a profile route. Profile is now available for all three roles and displays the logged-in user.
3. **Frontend silently accepted any login when the API was unavailable** — this could create a false authenticated state and route users into a dashboard without a real backend session. The fallback was removed; failed authentication now displays an error.
4. **Registration reported success even after an API failure** — the frontend now checks the HTTP response and shows an error instead of redirecting when registration fails.
5. **Missing Vite environment typings** — added `frontend/src/vite-env.d.ts` so `import.meta.env.VITE_API_URL` has the expected Vite typing.
6. **React Player API mismatch risk** — the project was using React Player v2's `url` prop while the maintained v3 API uses `src`. The dependency is updated to `3.4.x` and the player uses `src`.
7. **Missing Django app migrations** — the original project contained only `migrations/__init__.py`. A complete `0001_initial.py` covering the LMS models and the enrollment uniqueness constraint is now included.
8. **Windows MySQL driver installation friction** — the project now uses PyMySQL as the MySQL driver and registers it as the MySQLdb-compatible module. The database remains MySQL; this avoids requiring native `mysqlclient` compilation on typical Windows setups.
9. **Registration username handling was fragile** — the API now accepts an optional username, normalizes email addresses, prevents duplicate emails/usernames, and generates a unique username from the email when one is not provided.
10. **Server-owned API fields could be overwritten by clients** — notification user, support-ticket user, review student, and message sender are now read-only from the serializer/client side and are assigned from the authenticated request.
11. **Review ratings had no API range validation** — ratings are now constrained to 1–5 at the serializer validation layer.
12. **Django SQLite test configuration was not possible without editing settings** — `DB_ENGINE` is now configurable by environment while MySQL remains the default. This also makes local development/testing easier without changing the production database choice.

## Verification performed in this environment

- All backend `.py` files passed Python bytecode compilation (`compileall`).
- All frontend `.ts`/`.tsx` source files passed TypeScript transpilation/syntax validation with the installed TypeScript compiler.
- The original project could not complete `npm install` in this sandbox because the sandbox could not resolve `registry.npmjs.org`, so a full dependency-installed Vite/TypeScript build could not be executed here.
- Django itself was not installed in the sandbox, so `manage.py check/migrate/test` could not be executed here. The migration was therefore reviewed structurally against the model definitions and included as a normal initial migration.

## Runtime prerequisites

- Node.js: Vite 7 requires Node.js 20.19+ or 22.12+.
- Python: 3.11+ recommended by this project.
- MySQL: create the `heartify_lms` database before running migrations.
