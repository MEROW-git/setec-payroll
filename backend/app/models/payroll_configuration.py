from app.extensions import db
from app.models.base import BaseModel,SoftDeleteMixin
class PayrollCycle(BaseModel,SoftDeleteMixin):
 __tablename__="payroll_cycles"
 name=db.Column(db.String(150),unique=True,nullable=False);frequency=db.Column(db.String(30),nullable=False);pay_day=db.Column(db.Integer,nullable=False);is_default=db.Column(db.Boolean,nullable=False,default=False);is_active=db.Column(db.Boolean,nullable=False,default=True)
class TaxRule(BaseModel,SoftDeleteMixin):
 __tablename__="tax_rules"
 min_income=db.Column(db.Numeric(14,2),nullable=False);max_income=db.Column(db.Numeric(14,2));rate=db.Column(db.Numeric(6,3),nullable=False);description=db.Column(db.Text);is_active=db.Column(db.Boolean,nullable=False,default=True)
class PayrollPolicy(BaseModel,SoftDeleteMixin):
 __tablename__="payroll_policies"
 name=db.Column(db.String(150),unique=True,nullable=False);category=db.Column(db.String(30),nullable=False);count_type=db.Column(db.String(30),nullable=False);policy_type=db.Column(db.String(30),nullable=False);considerable_value=db.Column(db.Numeric(10,2),nullable=False);adjusted_value=db.Column(db.Numeric(12,2),nullable=False);value_mode=db.Column(db.String(20),nullable=False);description=db.Column(db.Text);is_active=db.Column(db.Boolean,nullable=False,default=True)
class PayrollSetting(BaseModel):
 __tablename__="payroll_settings"
 setting_key=db.Column(db.String(100),unique=True,nullable=False);setting_value=db.Column(db.JSON,nullable=False)
