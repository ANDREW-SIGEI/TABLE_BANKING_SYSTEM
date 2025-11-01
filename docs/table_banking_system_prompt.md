 # Table Banking System — Complete Implementation Prompt

## Purpose
This document captures the full scope, technical specifications, data models, APIs, PWA behaviors, integrations, security, and deployment requirements for the Table Banking System (ERPNext backend + Custom Frontend + Field Officer PWA). Use this as the primary prompt for developers and AI assistants to generate complete, production-ready code.

---

## Executive Summary
Build a comprehensive table banking management system with ERPNext/Frappe as the authoritative backend, React-based admin frontend, and Progressive Web App for field officers. The system must support offline-first operations, three loan types, mandatory ID verification, real-time officer tracking, and automated dividend calculations. Deployable on cloud platforms with full security and compliance.

---

## Primary Business Goals
- **Group & Member Management**: Complete registration with geo-location and next-of-kin details
- **Financial Operations**: Three loan types (short-term, long-term, project) with different calculation methods
- **Savings Tracking**: Comprehensive savings, welfare, and project fund management
- **Field Operations**: Offline-capable PWA for member registration, collections, and loan processing
- **Compliance Enforcement**: Mandatory ID capture (upload/live camera) before loan approval
- **Financial Reporting**: Dual-table accounting (Cash In/Out + TRF balances) per group
- **Automated Dividends**: Annual profit distribution based on member contributions
- **Officer Management**: Complete lifecycle from registration to activity tracking

---

## Technical Stack Specification

### Backend (ERPNext/Frappe)
- **Framework**: Frappe Framework v14+ with Python 3.8+
- **Database**: PostgreSQL (production), SQLite (development)
- **Queue & Cache**: Redis + RQ for background jobs
- **File Storage**: AWS S3 or MinIO for documents and images
- **API**: REST API with JWT authentication + Webhooks
- **Search**: Frappe full-text search with PostgreSQL

### Frontend (Admin Dashboard)
- **Framework**: React 18+ with TypeScript
- **State Management**: Redux Toolkit + RTK Query
- **UI Library**: Mantine UI v6+
- **Charts**: Chart.js with react-chartjs-2
- **Maps**: Leaflet/OpenStreetMap for officer tracking
- **Routing**: React Router v6

### Mobile (Field Officer PWA)
- **Core**: Progressive Web App with Service Worker
- **Offline Storage**: IndexedDB via localForage
- **Camera**: HTML5 Media API + Capacitor for native features
- **GPS**: Geolocation API with background sync
- **Push Notifications**: Firebase Cloud Messaging
- **State Management**: Zustand for lightweight state

### DevOps & Infrastructure
- **Containerization**: Docker + Docker Compose
- **CI/CD**: GitHub Actions with automated testing
- **Monitoring**: Prometheus + Grafana + Loki
- **Logging**: Structured JSON logging
- **Hosting**: AWS/DigitalOcean/Azure with load balancing

---

## Detailed Data Model

### Core Entities

#### BankingGroup
```python
{
    "name": "String (255)",
    "group_code": "String(50) UNIQUE",
    "county": "String(100)",
    "constituency": "String(100)", 
    "ward": "String(100)",
    "location": "String(100)",
    "village": "String(100)",
    "meeting_day": "String(20)",
    "meeting_venue": "String(255)",
    "registration_date": "Date",
    "status": "ACTIVE/INACTIVE"
}
```

#### GroupMember
```python
{
    "group": "ForeignKey(BankingGroup)",
    "member_name": "String(255)",
    "id_number": "String(50) UNIQUE",
    "phone": "String(20)",
    "date_of_birth": "Date",
    "registration_date": "Date",
    "is_active": "Boolean",
    "photo_url": "String",
    "id_document_url": "String",
    "next_of_kin": "JSON[]"  # {name, relationship, phone, id_number}
}
```

#### LoanApplication
```python
{
    "member": "ForeignKey(GroupMember)",
    "loan_type": "SHORT_TERM/LONG_TERM/PROJECT",
    "loan_amount": "Decimal(12,2)",
    "duration_months": "Integer",
    "interest_rate": "Decimal(5,2)",
    "purpose": "Text",
    "status": "PENDING/APPROVED/REJECTED/DISBURSED/COMPLETED",
    "application_date": "Date",
    "approved_date": "Date",
    "approved_by": "ForeignKey(User)",
    "id_verified": "Boolean",
    "witnesses": "JSON[]",  # member_ids
    "repayment_schedule": "JSON"  # calculated schedule
}
```

#### SavingsContribution
```python
{
    "member": "ForeignKey(GroupMember)",
    "amount": "Decimal(10,2)",
    "contribution_type": "REGULAR/WELFARE/PROJECT/FINE",
    "contribution_date": "Date",
    "recorded_by": "ForeignKey(User)",
    "payment_method": "CASH/MPESA/BANK",
    "offline_sync_id": "String"  # for conflict resolution
}
```

#### CashLedgerEntry
```python
{
    "group": "ForeignKey(BankingGroup)",
    "transaction_date": "Date",
    "category": "CASH_IN/CASH_OUT enum",
    "subcategory": "String",  # banking, short_term_loan, welfare, etc.
    "amount": "Decimal(12,2)",
    "description": "String(500)",
    "reference_doc": "String",  # link to loan/savings doc
    "balance_after": "Decimal(12,2)"
}
```

#### FieldOfficer
```python
{
    "user": "OneToOneField(User)",
    "phone": "String(20)",
    "assigned_groups": "ManyToManyField(BankingGroup)",
    "is_active": "Boolean",
    "last_known_location": "JSON",  # {lat, lng, timestamp}
    "device_info": "JSON"  # for PWA tracking
}
```

---

## Business Rules & Validation

### Loan Management
- **Eligibility**: Minimum 3 months consistent savings history
- **Amount Limits**: Maximum 3x member's total savings balance
- **Multiple Loans**: Only one active loan per member at a time
- **Approval Workflow**: 
  - < 50,000: Field Officer + Group Chair
  - 50,000-200,000: Field Officer + Group Committee  
  - > 200,000: Field Officer + Committee + System Admin

### Interest Calculations
```python
# Short-term (< 3 months)
def calculate_short_term(principal, interest_rate, duration):
    total_interest = principal * (interest_rate / 100)
    return principal + total_interest

# Long-term (Reducing Balance)
def calculate_long_term(principal, annual_rate, months, extra_payments=0):
    monthly_rate = annual_rate / 12 / 100
    schedule = []
    balance = principal
    
    for month in range(1, months + 1):
        interest = balance * monthly_rate
        principal_payment = (principal / months) + extra_payments
        total_payment = principal_payment + interest
        balance -= principal_payment
        
        schedule.append({
            'month': month,
            'principal': principal_payment,
            'interest': interest,
            'total_payment': total_payment,
            'remaining_balance': max(balance, 0)
        })
    
    return schedule
```

### Savings Rules
- **Minimum Contribution**: Configurable per group (default: KES 500/month)
- **Withdrawal Limits**: Maximum 50% of personal savings for emergencies
- **Welfare Fund**: Separate tracking with withdrawal conditions
- **Fines & Penalties**: Configurable amounts for late payments

### Dividend Distribution
```python
def calculate_dividends(group_id, fiscal_year):
    total_profit = get_total_profit(group_id, fiscal_year)
    total_savings = get_total_savings(group_id, fiscal_year)
    appreciation_fees = get_appreciation_fees(group_id, fiscal_year)
    
    distributable = (total_profit * 0.7) + appreciation_fees  # 70% to members
    
    members = get_active_members(group_id)
    for member in members:
        member_savings = get_member_savings(member.id, fiscal_year)
        share_percentage = (member_savings / total_savings) * 100
        dividend_amount = (distributable * share_percentage) / 100
        
        create_dividend_allocation(member.id, dividend_amount, fiscal_year)
```

---

## API Specification

### Authentication Endpoints
```python
# POST /api/auth/login
{
    "phone": "254712345678",
    "password": "secret123"
}

# Response
{
    "success": true,
    "access_token": "jwt_token_here",
    "refresh_token": "refresh_token_here",
    "user": {
        "id": "user_123",
        "name": "John Officer",
        "role": "FIELD_OFFICER",
        "assigned_groups": ["group_1", "group_2"]
    }
}
```

### Member Management
```python
# POST /api/members
{
    "group_id": "group_123",
    "member_name": "Jane Wanjiku",
    "id_number": "12345678",
    "phone": "254712345678",
    "date_of_birth": "1985-05-15",
    "next_of_kin": [
        {
            "name": "John Kamau",
            "relationship": "Spouse", 
            "phone": "254723456789",
            "id_number": "87654321"
        }
    ],
    "id_photo": "data:image/jpeg;base64,...",
    "signature": "data:image/png;base64,..."
}

# GET /api/groups/{id}/members
# GET /api/members/{id}/savings-summary
```

### Loan Operations
```python
# POST /api/loans
{
    "member_id": "member_123",
    "loan_type": "SHORT_TERM",
    "amount": 50000,
    "duration_months": 3,
    "purpose": "Business expansion",
    "witnesses": ["member_456", "member_789"],
    "id_documents": ["doc_1_url", "doc_2_url"]
}

# POST /api/loans/{id}/approve
{
    "approved_by": "user_123",
    "approval_notes": "Meeting minutes reference XYZ"
}

# POST /api/loans/{id}/repayment
{
    "amount": 5000,
    "payment_date": "2024-01-15",
    "payment_method": "MPESA",
    "transaction_id": "MPE123456"
}
```

### Savings & Transactions
```python
# POST /api/transactions
{
    "member_id": "member_123",
    "amount": 1500,
    "transaction_type": "DEPOSIT",
    "contribution_type": "REGULAR",
    "payment_method": "CASH",
    "offline_sync_id": "offline_123456"
}

# GET /api/groups/{id}/cash-ledger?from=2024-01-01&to=2024-01-31
# GET /api/groups/{id}/trf-balance
```

### Officer Tracking
```python
# POST /api/officers/{id}/track
{
    "latitude": -1.2921,
    "longitude": 36.8219,
    "accuracy": 15.5,
    "activity_type": "MEMBER_VISIT",
    "member_id": "member_123",
    "battery_level": 85
}

# GET /api/officers/active-locations
```

---

## PWA & Offline Sync Specification

### Offline Storage Schema
```javascript
// IndexedDB Structure
const dbSchema = {
    version: 1,
    stores: {
        pending_operations: {
            keyPath: 'id',
            indexes: ['type', 'timestamp', 'status']
        },
        members: {
            keyPath: 'id',
            indexes: ['group_id', 'phone']
        },
        savings_transactions: {
            keyPath: 'id', 
            indexes: ['member_id', 'date']
        },
        loan_applications: {
            keyPath: 'id',
            indexes: ['member_id', 'status']
        },
        sync_metadata: {
            keyPath: 'key'
        }
    }
};
```

### Sync Engine Logic
```javascript
class SyncEngine {
    async queueOperation(operation) {
        const operationWithMeta = {
            ...operation,
            id: generateUUID(),
            timestamp: new Date().toISOString(),
            status: 'pending',
            retry_count: 0
        };
        
        await this.db.pending_operations.add(operationWithMeta);
        await this.trySync();
    }
    
    async trySync() {
        if (!navigator.onLine) return;
        
        const pendingOps = await this.db.pending_operations
            .where('status').equals('pending')
            .toArray();
            
        for (const op of pendingOps) {
            try {
                await this.sendToServer(op);
                await this.db.pending_operations.delete(op.id);
            } catch (error) {
                op.retry_count += 1;
                op.last_error = error.message;
                if (op.retry_count >= 5) {
                    op.status = 'failed';
                }
                await this.db.pending_operations.put(op);
            }
        }
    }
    
    async sendToServer(operation) {
        const response = await fetch(`/api/${operation.type}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${await this.getToken()}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(operation.data)
        });
        
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json();
    }
}
```

### Background Sync
```javascript
// Service Worker
self.addEventListener('sync', (event) => {
    if (event.tag === 'background-sync') {
        event.waitUntil(syncEngine.trySync());
    }
});

// Periodic sync (every 15 minutes when online)
setInterval(() => {
    if (navigator.onLine) {
        syncEngine.trySync();
    }
}, 15 * 60 * 1000);
```

---

## Security & Compliance

### Authentication & Authorization
```python
# JWT Configuration
JWT_CONFIG = {
    'ALGORITHM': 'HS256',
    'ACCESS_TOKEN_EXPIRE_MINUTES': 30,
    'REFRESH_TOKEN_EXPIRE_DAYS': 7,
    'SECRET_KEY': 'environment_variable'
}

# Role-Based Access Control
ROLES = {
    'SYSTEM_ADMIN': ['*'],
    'FIELD_OFFICER': [
        'members:create', 'members:read',
        'loans:create', 'loans:read', 
        'transactions:create', 'transactions:read',
        'officer:track'
    ],
    'GROUP_CHAIR': [
        'loans:approve', 'members:read',
        'transactions:read', 'reports:read'
    ]
}
```

### Data Protection
- **Encryption**: AES-256 for PII at rest
- **TLS**: Enforce HTTPS everywhere
- **Data Retention**: 7 years for financial records
- **Backup**: Daily automated backups with encryption
- **Audit Logs**: Immutable logs for all financial transactions

### Compliance Requirements
- **GDPR/KDPA**: Right to erasure, data portability
- **Financial Regulations**: Interest rate caps, fee transparency
- **Accessibility**: WCAG 2.1 AA compliance
- **Audit**: Monthly financial reconciliation reports

---

## Integration Specifications

### M-Pesa Integration
```python
class MpesaService:
    def initiate_stk_push(self, phone, amount, account_ref):
        payload = {
            "BusinessShortCode": self.business_shortcode,
            "Password": self.generate_password(),
            "Timestamp": self.get_timestamp(),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": self.business_shortcode,
            "PhoneNumber": phone,
            "CallBackURL": f"{self.base_url}/api/mpesa/callback",
            "AccountReference": account_ref,
            "TransactionDesc": "Table Banking Contribution"
        }
        
        response = requests.post(
            f"{self.mpesa_url}/stkpush/v1/processrequest",
            json=payload,
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        return response.json()
    
    def handle_callback(self, callback_data):
        # Process M-Pesa callback and update transactions
        pass
```

### SMS/WhatsApp Integration
```python
class NotificationService:
    def send_loan_reminder(self, member, loan, days_overdue):
        message = f"Reminder: Loan repayment of KES {loan.due_amount} is {days_overdue} days overdue."
        self.send_sms(member.phone, message)
        
    def send_meeting_reminder(self, group, meeting):
        message = f"Reminder: {meeting.title} on {meeting.date} at {meeting.venue}"
        for member in group.members:
            self.send_sms(member.phone, message)
```

### PDF Generation
```python
class PDFService:
    def generate_loan_statement(self, loan):
        template = self.get_template('loan_statement.html')
        html = template.render(loan=loan, repayments=loan.repayments.all())
        return self.html_to_pdf(html)
    
    def generate_dividend_statement(self, member, dividend_year):
        template = self.get_template('dividend_statement.html')
        html = template.render(member=member, dividend=dividend_year)
        return self.html_to_pdf(html)
```

---

## Deployment & Infrastructure

### Docker Configuration
```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: tablebanking
      POSTGRES_USER: frappe
      POSTGRES_PASSWORD: frappe
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://frappe:frappe@postgres:5432/tablebanking
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  postgres_data:
```

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/tablebanking
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-django-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
ENCRYPTION_KEY=your-data-encryption-key

# Services
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
S3_BUCKET=tablebanking-files

# Integrations
MPESA_CONSUMER_KEY=your-consumer-key
MPESA_CONSUMER_SECRET=your-consumer-secret
MPESA_BUSINESS_SHORTCODE=123456
SMS_API_KEY=your-sms-api-key
```

---

## Testing Strategy

### Test Coverage Requirements
- **Unit Tests**: 90% coverage for business logic (loans, savings, dividends)
- **Integration Tests**: API endpoints, database operations, file uploads
- **E2E Tests**: Critical user journeys (registration → savings → loans → repayment)
- **Performance Tests**: Load testing for 100 concurrent officers

### Key Test Scenarios
```python
def test_loan_approval_workflow():
    # Setup
    member = create_member_with_savings()
    loan = create_loan_application(member)
    
    # Execute
    approve_loan(loan, approver=field_officer)
    disburse_loan(loan)
    
    # Verify
    assert loan.status == 'DISBURSED'
    assert cash_ledger_updated(loan.amount)
    assert member_loan_count(member) == 1

def test_offline_sync_recovery():
    # Setup offline scenario
    with network_disabled():
        transaction = record_savings_offline(member, 1000)
        assert transaction.offline_sync_id is not None
    
    # Reconnect and sync
    enable_network()
    wait_for_sync_completion()
    
    # Verify sync
    assert server_has_transaction(transaction.offline_sync_id)
```

---

## Success Metrics & Monitoring

### Business KPIs
- Member registration growth rate (monthly)
- Loan approval to disbursement time (target: < 48 hours)
- Loan repayment rate (target: > 95%)
- Officer activity rate (transactions per officer per day)

### Technical Metrics
- System uptime (target: 99.5%)
- API response time P95 (target: < 200ms)
- Offline sync success rate (target: > 99%)
- Data accuracy rate (target: 100%)

### User Experience
- Task completion rate for common operations
- Offline capability satisfaction scores
- Mobile app store ratings (if applicable)

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-4)
- Project setup and core infrastructure
- Basic member and group management
- Field officer authentication and basic PWA

### Phase 2: Financial Core (Weeks 5-8)
- Savings tracking and transactions
- Short-term loan management
- Basic reporting and dashboards

### Phase 3: Advanced Features (Weeks 9-12)
- Long-term and project loans
- Officer tracking and GPS integration
- Offline sync and conflict resolution

### Phase 4: Production Ready (Weeks 13-16)
- Dividend calculations and distributions
- M-Pesa and SMS integrations
- Security hardening and performance optimization

### Phase 5: Scale & Enhance (Weeks 17-20)
- Advanced analytics and reporting
- Mobile app store deployment (if needed)
- Multi-language and localization

---

## Risk Mitigation

### Technical Risks
- **Data Loss**: Automated backups with regular recovery testing
- **Security Breaches**: Regular security audits and penetration testing
- **Performance Issues**: Proactive monitoring and auto-scaling

### Business Risks
- **Fraud Prevention**: Multi-level approval workflows and audit trails
- **Regulatory Changes**: Regular compliance reviews and legal consultations
- **Vendor Dependencies**: Fallback mechanisms for third-party services

### Operational Risks
- **Staff Training**: Comprehensive documentation and training programs
- **Business Continuity**: Disaster recovery and business continuity planning
- **Scalability Issues**: Regular capacity planning and performance testing

---

## Deliverables Checklist

- [ ] Complete source code with documentation
- [ ] Database schema and migration scripts
- [ ] API documentation with examples
- [ ] Deployment and setup guides
- [ ] User manuals for admins and field officers
- [ ] Testing suite and quality reports
- [ ] Security and compliance documentation
- [ ] Monitoring and maintenance guides

---

_This prompt provides complete specifications for building a production-ready Table Banking System. Use it to generate code, tests, documentation, and deployment configurations._
