# Project Rebuild Plan — Book Club App

Tracking the rebuild from Library Management System → Book Club App
using the previous database schema (Project 3).

---

## Backend

| Task | File | Status |
|---|---|---|
| Rewrite models for 7-table book club schema | `models.py` | Done |
| Rewrite all routes for new schema | `app.py` | Done |

---

## Templates

### Keep / Minor Update
| Template | Status |
|---|---|
| `base.html` — update navbar links | Not done |
| `member_form.html` — works as-is | Done |

### Full Rewrite
| Template | Status |
|---|---|
| `dashboard.html` — new stats (clubs, reviews, avg rating, reading progress) | Not done |
| `members.html` — remove loan count column | Not done |
| `books.html` — remove availability columns, add genre/year | Not done |
| `book_form.html` — replace author dropdown with text field, add ISBN/pages/year | Not done |
| `book_detail.html` — show reviews instead of loan info | Not done |

### New Templates
| Template | Status |
|---|---|
| `clubs.html` — list all clubs | Not done |
| `club_form.html` — add/edit club | Not done |
| `club_detail.html` — show members + meetings for a club | Not done |
| `join_form.html` — add member to club | Not done |
| `progress.html` — list all reading progress records | Not done |
| `progress_form.html` — log/update reading progress | Not done |
| `reviews.html` — list all reviews | Not done |
| `review_form.html` — add a review | Not done |
| `meetings.html` — list all meetings | Not done |
| `meeting_form.html` — add a meeting | Not done |

---

## Documentation

| Task | File | Status |
|---|---|---|
| Update schema to book club tables | `schema.sql` | Not done |
| Update normalization report for new schema | `NORMALIZATION.md` | Not done |
| Update README for book club app | `README.md` | Not done |
| Delete old `library.db` before running | local only | Not done |

---

## Summary

| Category | Done | Remaining |
|---|---|---|
| Backend | 2 | 0 |
| Templates | 2 | 10 |
| Documentation | 0 | 3 |
| **Total** | **4** | **13** |

---

## Next Up
1. `base.html` — update navbar (quick)
2. Dashboard template
3. Books templates (list, form, detail)
4. Clubs templates (list, form, detail)
5. Memberships (join form)
6. Progress templates
7. Reviews templates
8. Meetings templates
9. Update `schema.sql`, `NORMALIZATION.md`, `README.md`
