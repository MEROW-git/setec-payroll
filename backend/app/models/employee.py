from app.extensions import db
from app.models.base import BaseModel, SoftDeleteMixin, UnsignedBigInteger


class Employee(BaseModel, SoftDeleteMixin):
    __tablename__ = "employees"
    __table_args__ = (
        db.Index("ix_employees_employee_code", "employee_code"),
        db.Index("ix_employees_department_id", "department_id"),
        db.Index("ix_employees_position_id", "position_id"),
        db.Index("ix_employees_manager_id", "manager_id"),
        db.Index("ix_employees_employment_status", "employment_status"),
        db.Index("ix_employees_hire_date", "hire_date"),
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    user_id = db.Column(UnsignedBigInteger, db.ForeignKey("users.id", ondelete="SET NULL"), unique=True)
    department_id = db.Column(UnsignedBigInteger, db.ForeignKey("departments.id", ondelete="RESTRICT"), nullable=False)
    position_id = db.Column(UnsignedBigInteger, db.ForeignKey("positions.id", ondelete="RESTRICT"), nullable=False)
    manager_id = db.Column(UnsignedBigInteger, db.ForeignKey("employees.id", ondelete="SET NULL"))
    employee_code = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    phone = db.Column(db.String(30))
    personal_email = db.Column(db.String(191))
    work_email = db.Column(db.String(191), unique=True)
    address = db.Column(db.Text)
    profile_photo = db.Column(db.String(500))
    hire_date = db.Column(db.Date, nullable=False)
    probation_end_date = db.Column(db.Date)
    employment_status = db.Column(db.String(30), default="active", nullable=False)
    employment_type = db.Column(db.String(30), default="full_time", nullable=False)
    basic_salary = db.Column(db.Numeric(12, 2), default=0, nullable=False)
    bank_name = db.Column(db.String(150))
    bank_account_name = db.Column(db.String(150))
    bank_account_number = db.Column(db.String(100))
    emergency_contact_name = db.Column(db.String(150))
    emergency_contact_phone = db.Column(db.String(30))

    user = db.relationship("User", back_populates="employee")
    department = db.relationship("Department", foreign_keys=[department_id], back_populates="employees")
    position = db.relationship("Position", back_populates="employees")
    manager = db.relationship("Employee", remote_side="Employee.id", back_populates="subordinates")
    subordinates = db.relationship("Employee", back_populates="manager")
    documents = db.relationship("EmployeeDocument", back_populates="employee", cascade="all, delete-orphan")
    attendance_records = db.relationship("Attendance", back_populates="employee", cascade="all, delete-orphan")
    leave_requests = db.relationship("LeaveRequest", back_populates="employee", cascade="all, delete-orphan")
    payrolls = db.relationship("Payroll", back_populates="employee", cascade="all, delete-orphan")
    salary_components = db.relationship("EmployeeSalaryComponent", back_populates="employee", cascade="all, delete-orphan")
    performance_reviews = db.relationship(
        "PerformanceReview",
        foreign_keys="PerformanceReview.employee_id",
        back_populates="employee",
        cascade="all, delete-orphan",
    )
    reviews_given = db.relationship(
        "PerformanceReview",
        foreign_keys="PerformanceReview.reviewer_id",
        back_populates="reviewer",
    )
