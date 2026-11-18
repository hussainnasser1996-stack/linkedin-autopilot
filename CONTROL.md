# CONTROL — change these lines to steer the autopilot (from your phone: ask Claude, or edit on github.com)

mode: auto
# auto   = posts are scheduled in Buffer without asking (standing approval)
# review = posts are created in Buffer as DRAFTS; nothing publishes until you approve in the Buffer app
# paused = the routine does nothing

arabic_mode: review
# review = Friday Arabic posts are saved as Buffer DRAFTS for Hussain to approve; auto = scheduled like the rest

approval_until: 2026-12-31
# In auto mode, standing approval ends on this date; after it the routine switches itself to review.

focus_this_week:
# optional free text, e.g. "more gaming", "cover Aramco results Tuesday", "no AI posts"

skip_dates:
- 2026-11-19  # his Al Arabiya GTA VI clip goes out by hand that day
# optional list of YYYY-MM-DD dates with no post
