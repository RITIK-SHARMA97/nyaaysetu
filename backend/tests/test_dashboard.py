from datetime import datetime, timedelta
import uuid

from app.models.action import ActionItem
from app.models.compliance import ComplianceHealth
from app.workers.escalation import _refresh_leaderboard


def test_refresh_leaderboard_preserves_seeded_demo_score(test_db):
    test_db.query(ActionItem).delete()
    test_db.query(ComplianceHealth).delete()
    test_db.commit()

    dept = 'Revenue Department'
    test_db.add_all([
        ActionItem(
            id=str(uuid.uuid4()),
            judgment_id='judgment-1',
            directive_text='Directive 1',
            responsible_department=dept,
            due_date=(datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'),
            days_left=-3,
            contempt_risk='critical',
            status='in_progress',
        ),
        ActionItem(
            id=str(uuid.uuid4()),
            judgment_id='judgment-1',
            directive_text='Directive 2',
            responsible_department=dept,
            due_date=(datetime.now() + timedelta(days=4)).strftime('%Y-%m-%d'),
            days_left=4,
            contempt_risk='critical',
            status='approved',
        ),
        ComplianceHealth(
            id=str(uuid.uuid4()),
            department=dept,
            total_actions=2,
            complied_actions=0,
            overdue_actions=1,
            critical_actions=2,
            compliance_score=34.0,
            trend='worsening',
        ),
    ])
    test_db.commit()

    _refresh_leaderboard(test_db)

    refreshed = test_db.query(ComplianceHealth).filter(ComplianceHealth.department == dept).one()
    assert refreshed.total_actions == 2
    assert refreshed.overdue_actions == 1
    assert refreshed.critical_actions == 2
    assert refreshed.compliance_score == 34.0
    assert refreshed.trend == 'worsening'
