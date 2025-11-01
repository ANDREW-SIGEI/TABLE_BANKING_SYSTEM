# Implementation Checklist — Table Banking System

This checklist breaks the project into actionable tasks and suggested owners (Backend, Frontend, PWA, DevOps).

## Phase 0 — Setup
- [ ] Create repo structure and docs (done)
- [ ] Cloud account & basic infra (VPC, DB, Object Storage)
- [ ] Configure CI/CD (GitHub Actions / GitLab CI)

## Phase 1 — Core Models & Backend
- [ ] Create ERPNext/Frappe DocTypes: Group, Member, Loan, Savings, CashLedgerEntry, TRFEntry, MeetingSchedule, DividendYearly
- [ ] Implement REST API endpoints for core CRUD
- [ ] Implement auth (JWT/session) and role permissions

## Phase 2 — Frontend & PWA MVP
- [ ] Build React app scaffold (routing, auth)
- [ ] Build Member registration UI + ID upload
- [ ] Build Field Officer PWA with offline queue (IndexedDB)
- [ ] Sync engine and conflict handling

## Phase 3 — Loans & Accounting
- [ ] Short-term loan flow: create, approve, disburse, repay
- [ ] Long-term loan amortization (reducing balance)
- [ ] Project loan workflow (product financing)
- [ ] Cash in / Cash out ledger and TRF mapping

## Phase 4 — Meetings & Attendance
- [ ] Meeting scheduling UI and attendance capture
- [ ] Reports for attendance vs collections

## Phase 5 — Integrations & Ops
- [ ] M-Pesa integration and webhook handling
- [ ] SMS/WhatsApp integration for reminders
- [ ] PDF generation for statements and receipts
- [ ] Backups, monitoring, and production deployment

## Phase 6 — Reports & Dividends
- [ ] Dividend calculation engine and yearly report
- [ ] Admin UI to trigger and review distributions

## QA & Testing
- [ ] Unit tests for accounting & amortization
- [ ] Integration tests for sync engine
- [ ] E2E tests for critical flows

## Post-Launch
- [ ] Collect user feedback from field officers
- [ ] Iterate UX for offline flows
- [ ] Add analytics and loan risk models


> Notes: adapt sprint lengths to team size. Prioritize a working PWA that supports member registration, savings recording, and short-term loans for the MVP.
