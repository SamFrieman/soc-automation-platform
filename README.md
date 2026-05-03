<div align="center">

# SOC Automation Platform

**Modular SOAR platform for alert ingestion, threat enrichment, and case management**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://python.org)
[![Django](https://img.shields.io/badge/Django-REST-green?logo=django)](https://djangoproject.com)
[![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react)](https://react.dev)
[![Celery](https://img.shields.io/badge/Celery-Async-37814A?logo=celery)](https://docs.celeryq.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## Overview

A Security Operations Center automation platform that handles the full alert lifecycle — from ingestion through enrichment, triage, and case creation. Playbooks are mapped to industry frameworks so analysts always know where a finding fits in the threat landscape.

**Framework coverage:** MITRE ATT&CK · MITRE D3FEND · Kill Chain · Diamond Model · OWASP Top 10 · STRIDE

---

## Architecture

```
Django REST API  ──┐
                   ├── PostgreSQL (case/alert storage)
React Frontend  ──┘
                   
Celery Workers  ──── Redis Broker (async task queue)
Celery Beat     ──── Scheduled enrichment jobs
```

**Alert lifecycle:**
1. Alert ingested via REST API or webhook
2. Celery worker triggers enrichment (IOC lookup, ATT&CK mapping, severity scoring)
3. Case auto-created with linked evidence and framework tags
4. Analyst reviews in React dashboard; playbook recommendations surfaced inline
5. Case closed with disposition + TTPs logged for trending

---

## Features

- **Async alert ingestion** — Celery + Redis queue handles burst ingestion without blocking the API
- **Threat enrichment** — automated IOC context, MITRE technique tagging, severity classification
- **Reusable playbooks** — mapped to ATT&CK, D3FEND, Diamond Model, OWASP Top 10, STRIDE
- **Case management** — structured case creation, evidence linking, disposition tracking
- **Framework data loader** — one command populates ATT&CK techniques, Kill Chain phases, Diamond Model components
- **pytest + npm test** — backend and frontend test suites included

---

## Quick Start

**Requirements:** Python 3.9+, Node 16+, PostgreSQL 12+, Redis 6+

```bash
git clone https://github.com/SamFrieman/soc-automation-platform
cd soc-automation-platform

# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # set DATABASE_URL, REDIS_URL, SECRET_KEY

python manage.py migrate
python manage.py load_frameworks  # populate ATT&CK, Kill Chain, Diamond Model, STRIDE, OWASP

# Start services (separate terminals)
redis-server
celery -A soc_platform worker --loglevel=info
python manage.py runserver

# Frontend
cd ../frontend
npm install && npm start
```

---

## Framework Mappings

Each alert and playbook is tagged with relevant techniques from multiple frameworks simultaneously:

| Framework | Coverage |
|-----------|----------|
| MITRE ATT&CK | Tactic + technique + sub-technique |
| MITRE D3FEND | Defensive countermeasure mapping |
| Cyber Kill Chain | Stage classification |
| Diamond Model | Adversary / capability / infrastructure / victim |
| OWASP Top 10 | Web vulnerability classification |
| STRIDE | Threat modeling category |

---

## Deployment

**Cloud (Heroku / AWS / Azure / DigitalOcean):**
```bash
# Configure environment variables, run migrations, start gunicorn + celery via systemd
```

**CI/CD:** GitHub Actions workflows included for automated testing and deployment.

---

## License

MIT
