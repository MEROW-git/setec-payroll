"""initial hrm schema

Revision ID: 0001_initial_hrm_schema
Revises:
Create Date: 2026-07-10
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision = "0001_initial_hrm_schema"
down_revision = None
branch_labels = None
depends_on = None

BIGINT_UNSIGNED = mysql.BIGINT(unsigned=True)
TABLE_KWARGS = {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"}


def id_column():
    return sa.Column("id", BIGINT_UNSIGNED, primary_key=True, autoincrement=True)


def timestamps(soft_delete=False, updated=True):
    cols = [
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    ]
    if updated:
        cols.append(
            sa.Column(
                "updated_at",
                sa.DateTime(),
                nullable=False,
                server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
            )
        )
    if soft_delete:
        cols.append(sa.Column("deleted_at", sa.DateTime(), nullable=True))
    return cols


def fk(name, referred_table, ondelete):
    return sa.ForeignKeyConstraint([name], [f"{referred_table}.id"], ondelete=ondelete)


def money(name, default="0.00", nullable=False):
    return sa.Column(name, sa.Numeric(12, 2), nullable=nullable, server_default=sa.text(default))


def upgrade():
    op.create_table(
        "roles",
        id_column(),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        *timestamps(soft_delete=True),
        sa.UniqueConstraint("name", name="uq_roles_name"),
        **TABLE_KWARGS,
    )

    op.create_table(
        "users",
        id_column(),
        sa.Column("role_id", BIGINT_UNSIGNED, nullable=False),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("email", sa.String(191), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("last_login_at", sa.DateTime(), nullable=True),
        *timestamps(soft_delete=True),
        fk("role_id", "roles", "RESTRICT"),
        sa.UniqueConstraint("email", name="uq_users_email"),
        sa.Index("ix_users_role_id", "role_id"),
        sa.Index("ix_users_email", "email"),
        sa.Index("ix_users_is_active", "is_active"),
        **TABLE_KWARGS,
    )

    op.create_table(
        "departments",
        id_column(),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("code", sa.String(30), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("manager_employee_id", BIGINT_UNSIGNED, nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        *timestamps(soft_delete=True),
        sa.UniqueConstraint("name", name="uq_departments_name"),
        sa.UniqueConstraint("code", name="uq_departments_code"),
        sa.Index("ix_departments_manager_employee_id", "manager_employee_id"),
        sa.Index("ix_departments_is_active", "is_active"),
        **TABLE_KWARGS,
    )

    op.create_table(
        "positions",
        id_column(),
        sa.Column("department_id", BIGINT_UNSIGNED, nullable=False),
        sa.Column("title", sa.String(150), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        money("min_salary", nullable=True),
        money("max_salary", nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        *timestamps(soft_delete=True),
        fk("department_id", "departments", "RESTRICT"),
        sa.UniqueConstraint("department_id", "title", name="uq_positions_department_title"),
        sa.CheckConstraint("min_salary IS NULL OR max_salary IS NULL OR min_salary <= max_salary", name="ck_positions_salary_range"),
        sa.Index("ix_positions_department_id", "department_id"),
        sa.Index("ix_positions_is_active", "is_active"),
        **TABLE_KWARGS,
    )

    op.create_table(
        "employees",
        id_column(),
        sa.Column("user_id", BIGINT_UNSIGNED, nullable=True),
        sa.Column("department_id", BIGINT_UNSIGNED, nullable=False),
        sa.Column("position_id", BIGINT_UNSIGNED, nullable=False),
        sa.Column("manager_id", BIGINT_UNSIGNED, nullable=True),
        sa.Column("employee_code", sa.String(50), nullable=False),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("gender", sa.String(20), nullable=True),
        sa.Column("date_of_birth", sa.Date(), nullable=True),
        sa.Column("phone", sa.String(30), nullable=True),
        sa.Column("personal_email", sa.String(191), nullable=True),
        sa.Column("work_email", sa.String(191), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("profile_photo", sa.String(500), nullable=True),
        sa.Column("hire_date", sa.Date(), nullable=False),
        sa.Column("probation_end_date", sa.Date(), nullable=True),
        sa.Column("employment_status", sa.String(30), nullable=False, server_default="active"),
        sa.Column("employment_type", sa.String(30), nullable=False, server_default="full_time"),
        money("basic_salary"),
        sa.Column("bank_name", sa.String(150), nullable=True),
        sa.Column("bank_account_name", sa.String(150), nullable=True),
        sa.Column("bank_account_number", sa.String(100), nullable=True),
        sa.Column("emergency_contact_name", sa.String(150), nullable=True),
        sa.Column("emergency_contact_phone", sa.String(30), nullable=True),
        *timestamps(soft_delete=True),
        fk("user_id", "users", "SET NULL"),
        fk("department_id", "departments", "RESTRICT"),
        fk("position_id", "positions", "RESTRICT"),
        fk("manager_id", "employees", "SET NULL"),
        sa.UniqueConstraint("user_id", name="uq_employees_user_id"),
        sa.UniqueConstraint("employee_code", name="uq_employees_employee_code"),
        sa.UniqueConstraint("work_email", name="uq_employees_work_email"),
        sa.Index("ix_employees_employee_code", "employee_code"),
        sa.Index("ix_employees_department_id", "department_id"),
        sa.Index("ix_employees_position_id", "position_id"),
        sa.Index("ix_employees_manager_id", "manager_id"),
        sa.Index("ix_employees_employment_status", "employment_status"),
        sa.Index("ix_employees_hire_date", "hire_date"),
        **TABLE_KWARGS,
    )

    op.create_foreign_key(
        "fk_departments_manager_employee_id",
        "departments",
        "employees",
        ["manager_employee_id"],
        ["id"],
        ondelete="SET NULL",
    )

    op.create_table(
        "employee_documents",
        id_column(),
        sa.Column("employee_id", BIGINT_UNSIGNED, nullable=False),
        sa.Column("document_type", sa.String(100), nullable=False),
        sa.Column("document_name", sa.String(255), nullable=False),
        sa.Column("file_path", sa.String(500), nullable=False),
        sa.Column("issue_date", sa.Date(), nullable=True),
        sa.Column("expiry_date", sa.Date(), nullable=True),
        sa.Column("uploaded_by", BIGINT_UNSIGNED, nullable=True),
        *timestamps(soft_delete=True),
        fk("employee_id", "employees", "CASCADE"),
        fk("uploaded_by", "users", "SET NULL"),
        sa.Index("ix_employee_documents_employee_id", "employee_id"),
        sa.Index("ix_employee_documents_document_type", "document_type"),
        sa.Index("ix_employee_documents_expiry_date", "expiry_date"),
        **TABLE_KWARGS,
    )

    op.create_table(
        "attendance",
        id_column(),
        sa.Column("employee_id", BIGINT_UNSIGNED, nullable=False),
        sa.Column("attendance_date", sa.Date(), nullable=False),
        sa.Column("check_in", sa.DateTime(), nullable=True),
        sa.Column("check_out", sa.DateTime(), nullable=True),
        sa.Column("work_minutes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("overtime_minutes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(30), nullable=False, server_default="present"),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("approved_by", BIGINT_UNSIGNED, nullable=True),
        *timestamps(),
        fk("employee_id", "employees", "CASCADE"),
        fk("approved_by", "users", "SET NULL"),
        sa.UniqueConstraint("employee_id", "attendance_date", name="uq_attendance_employee_date"),
        sa.CheckConstraint("work_minutes >= 0", name="ck_attendance_work_minutes_nonnegative"),
        sa.CheckConstraint("overtime_minutes >= 0", name="ck_attendance_overtime_minutes_nonnegative"),
        sa.Index("ix_attendance_attendance_date", "attendance_date"),
        sa.Index("ix_attendance_employee_id", "employee_id"),
        sa.Index("ix_attendance_status", "status"),
        **TABLE_KWARGS,
    )

    op.create_table(
        "leave_types",
        id_column(),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("code", sa.String(30), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("days_per_year", sa.Numeric(5, 2), nullable=False, server_default="0.00"),
        sa.Column("is_paid", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("requires_attachment", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        *timestamps(soft_delete=True),
        sa.UniqueConstraint("name", name="uq_leave_types_name"),
        sa.UniqueConstraint("code", name="uq_leave_types_code"),
        **TABLE_KWARGS,
    )

    op.create_table(
        "leave_requests",
        id_column(),
        sa.Column("employee_id", BIGINT_UNSIGNED, nullable=False),
        sa.Column("leave_type_id", BIGINT_UNSIGNED, nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("total_days", sa.Numeric(5, 2), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("attachment_path", sa.String(500), nullable=True),
        sa.Column("status", sa.String(30), nullable=False, server_default="pending"),
        sa.Column("reviewed_by", BIGINT_UNSIGNED, nullable=True),
        sa.Column("reviewed_at", sa.DateTime(), nullable=True),
        sa.Column("reviewer_note", sa.Text(), nullable=True),
        *timestamps(soft_delete=True),
        fk("employee_id", "employees", "CASCADE"),
        fk("leave_type_id", "leave_types", "RESTRICT"),
        fk("reviewed_by", "users", "SET NULL"),
        sa.CheckConstraint("end_date >= start_date", name="ck_leave_requests_date_range"),
        sa.CheckConstraint("total_days > 0", name="ck_leave_requests_total_days_positive"),
        sa.Index("ix_leave_requests_employee_id", "employee_id"),
        sa.Index("ix_leave_requests_leave_type_id", "leave_type_id"),
        sa.Index("ix_leave_requests_status", "status"),
        sa.Index("ix_leave_requests_start_date", "start_date"),
        sa.Index("ix_leave_requests_end_date", "end_date"),
        **TABLE_KWARGS,
    )

    op.create_table(
        "holidays",
        id_column(),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("holiday_date", sa.Date(), nullable=False),
        sa.Column("is_paid", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("description", sa.Text(), nullable=True),
        *timestamps(),
        sa.UniqueConstraint("holiday_date", name="uq_holidays_holiday_date"),
        sa.Index("ix_holidays_holiday_date", "holiday_date"),
        **TABLE_KWARGS,
    )

    op.create_table(
        "payroll_periods",
        id_column(),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("pay_date", sa.Date(), nullable=True),
        sa.Column("status", sa.String(30), nullable=False, server_default="draft"),
        sa.Column("created_by", BIGINT_UNSIGNED, nullable=True),
        sa.Column("finalized_by", BIGINT_UNSIGNED, nullable=True),
        sa.Column("finalized_at", sa.DateTime(), nullable=True),
        *timestamps(),
        fk("created_by", "users", "SET NULL"),
        fk("finalized_by", "users", "SET NULL"),
        sa.UniqueConstraint("start_date", "end_date", name="uq_payroll_periods_start_end"),
        sa.CheckConstraint("end_date >= start_date", name="ck_payroll_periods_date_range"),
        sa.Index("ix_payroll_periods_status", "status"),
        sa.Index("ix_payroll_periods_start_date", "start_date"),
        sa.Index("ix_payroll_periods_end_date", "end_date"),
        **TABLE_KWARGS,
    )

    op.create_table(
        "payrolls",
        id_column(),
        sa.Column("payroll_period_id", BIGINT_UNSIGNED, nullable=False),
        sa.Column("employee_id", BIGINT_UNSIGNED, nullable=False),
        money("basic_salary"),
        money("total_allowance"),
        money("overtime_pay"),
        money("bonus"),
        money("gross_salary"),
        money("total_deduction"),
        money("tax_amount"),
        money("net_salary"),
        sa.Column("payment_status", sa.String(30), nullable=False, server_default="unpaid"),
        sa.Column("paid_at", sa.DateTime(), nullable=True),
        sa.Column("payment_reference", sa.String(150), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        *timestamps(),
        fk("payroll_period_id", "payroll_periods", "CASCADE"),
        fk("employee_id", "employees", "CASCADE"),
        sa.UniqueConstraint("payroll_period_id", "employee_id", name="uq_payrolls_period_employee"),
        sa.CheckConstraint("basic_salary >= 0", name="ck_payrolls_basic_salary_nonnegative"),
        sa.CheckConstraint("total_allowance >= 0", name="ck_payrolls_total_allowance_nonnegative"),
        sa.CheckConstraint("overtime_pay >= 0", name="ck_payrolls_overtime_pay_nonnegative"),
        sa.CheckConstraint("bonus >= 0", name="ck_payrolls_bonus_nonnegative"),
        sa.CheckConstraint("gross_salary >= 0", name="ck_payrolls_gross_salary_nonnegative"),
        sa.CheckConstraint("total_deduction >= 0", name="ck_payrolls_total_deduction_nonnegative"),
        sa.CheckConstraint("tax_amount >= 0", name="ck_payrolls_tax_amount_nonnegative"),
        sa.CheckConstraint("net_salary >= 0", name="ck_payrolls_net_salary_nonnegative"),
        sa.Index("ix_payrolls_employee_id", "employee_id"),
        sa.Index("ix_payrolls_payroll_period_id", "payroll_period_id"),
        sa.Index("ix_payrolls_payment_status", "payment_status"),
        **TABLE_KWARGS,
    )

    op.create_table(
        "salary_components",
        id_column(),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("code", sa.String(50), nullable=False),
        sa.Column("component_type", sa.String(30), nullable=False),
        sa.Column("calculation_type", sa.String(30), nullable=False, server_default="fixed"),
        money("default_amount"),
        sa.Column("is_taxable", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        *timestamps(soft_delete=True),
        sa.UniqueConstraint("name", name="uq_salary_components_name"),
        sa.UniqueConstraint("code", name="uq_salary_components_code"),
        sa.CheckConstraint("default_amount >= 0", name="ck_salary_components_default_amount_nonnegative"),
        sa.Index("ix_salary_components_component_type", "component_type"),
        sa.Index("ix_salary_components_is_active", "is_active"),
        **TABLE_KWARGS,
    )

    op.create_table(
        "employee_salary_components",
        id_column(),
        sa.Column("employee_id", BIGINT_UNSIGNED, nullable=False),
        sa.Column("salary_component_id", BIGINT_UNSIGNED, nullable=False),
        money("amount"),
        sa.Column("effective_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        *timestamps(soft_delete=True),
        fk("employee_id", "employees", "CASCADE"),
        fk("salary_component_id", "salary_components", "RESTRICT"),
        sa.CheckConstraint("amount >= 0", name="ck_employee_salary_components_amount_nonnegative"),
        sa.Index("ix_employee_salary_components_employee_id", "employee_id"),
        sa.Index("ix_employee_salary_components_salary_component_id", "salary_component_id"),
        sa.Index("ix_employee_salary_components_effective_date", "effective_date"),
        sa.Index("ix_employee_salary_components_is_active", "is_active"),
        **TABLE_KWARGS,
    )

    op.create_table(
        "performance_reviews",
        id_column(),
        sa.Column("employee_id", BIGINT_UNSIGNED, nullable=False),
        sa.Column("reviewer_id", BIGINT_UNSIGNED, nullable=False),
        sa.Column("review_date", sa.Date(), nullable=False),
        sa.Column("review_period_start", sa.Date(), nullable=True),
        sa.Column("review_period_end", sa.Date(), nullable=True),
        sa.Column("score", sa.Numeric(5, 2), nullable=True),
        sa.Column("strengths", sa.Text(), nullable=True),
        sa.Column("improvements", sa.Text(), nullable=True),
        sa.Column("comments", sa.Text(), nullable=True),
        sa.Column("status", sa.String(30), nullable=False, server_default="draft"),
        *timestamps(soft_delete=True),
        fk("employee_id", "employees", "CASCADE"),
        fk("reviewer_id", "employees", "RESTRICT"),
        sa.Index("ix_performance_reviews_employee_id", "employee_id"),
        sa.Index("ix_performance_reviews_reviewer_id", "reviewer_id"),
        sa.Index("ix_performance_reviews_review_date", "review_date"),
        sa.Index("ix_performance_reviews_status", "status"),
        **TABLE_KWARGS,
    )

    op.create_table(
        "announcements",
        id_column(),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("audience_type", sa.String(30), nullable=False, server_default="all"),
        sa.Column("department_id", BIGINT_UNSIGNED, nullable=True),
        sa.Column("published_by", BIGINT_UNSIGNED, nullable=False),
        sa.Column("published_at", sa.DateTime(), nullable=True),
        sa.Column("expires_at", sa.DateTime(), nullable=True),
        sa.Column("status", sa.String(30), nullable=False, server_default="draft"),
        *timestamps(soft_delete=True),
        fk("department_id", "departments", "SET NULL"),
        fk("published_by", "users", "RESTRICT"),
        sa.Index("ix_announcements_department_id", "department_id"),
        sa.Index("ix_announcements_status", "status"),
        sa.Index("ix_announcements_published_at", "published_at"),
        **TABLE_KWARGS,
    )

    op.create_table(
        "job_openings",
        id_column(),
        sa.Column("department_id", BIGINT_UNSIGNED, nullable=False),
        sa.Column("position_id", BIGINT_UNSIGNED, nullable=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("requirements", sa.Text(), nullable=True),
        sa.Column("employment_type", sa.String(30), nullable=False, server_default="full_time"),
        sa.Column("location", sa.String(200), nullable=True),
        money("min_salary", nullable=True),
        money("max_salary", nullable=True),
        sa.Column("openings_count", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("closing_date", sa.Date(), nullable=True),
        sa.Column("status", sa.String(30), nullable=False, server_default="draft"),
        sa.Column("created_by", BIGINT_UNSIGNED, nullable=True),
        *timestamps(soft_delete=True),
        fk("department_id", "departments", "RESTRICT"),
        fk("position_id", "positions", "SET NULL"),
        fk("created_by", "users", "SET NULL"),
        sa.CheckConstraint("min_salary IS NULL OR max_salary IS NULL OR min_salary <= max_salary", name="ck_job_openings_salary_range"),
        sa.Index("ix_job_openings_department_id", "department_id"),
        sa.Index("ix_job_openings_position_id", "position_id"),
        sa.Index("ix_job_openings_status", "status"),
        sa.Index("ix_job_openings_closing_date", "closing_date"),
        **TABLE_KWARGS,
    )

    op.create_table(
        "candidates",
        id_column(),
        sa.Column("job_opening_id", BIGINT_UNSIGNED, nullable=False),
        sa.Column("full_name", sa.String(200), nullable=False),
        sa.Column("email", sa.String(191), nullable=True),
        sa.Column("phone", sa.String(30), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("cv_file_path", sa.String(500), nullable=True),
        sa.Column("cover_letter", sa.Text(), nullable=True),
        sa.Column("years_experience", sa.Numeric(5, 2), nullable=True),
        money("expected_salary", nullable=True),
        sa.Column("status", sa.String(30), nullable=False, server_default="applied"),
        sa.Column("applied_at", sa.DateTime(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        *timestamps(soft_delete=True),
        fk("job_opening_id", "job_openings", "CASCADE"),
        sa.Index("ix_candidates_job_opening_id", "job_opening_id"),
        sa.Index("ix_candidates_email", "email"),
        sa.Index("ix_candidates_status", "status"),
        sa.Index("ix_candidates_applied_at", "applied_at"),
        **TABLE_KWARGS,
    )

    op.create_table(
        "audit_logs",
        id_column(),
        sa.Column("user_id", BIGINT_UNSIGNED, nullable=True),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("entity_type", sa.String(100), nullable=False),
        sa.Column("entity_id", BIGINT_UNSIGNED, nullable=True),
        sa.Column("old_values", sa.JSON(), nullable=True),
        sa.Column("new_values", sa.JSON(), nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("user_agent", sa.String(500), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        fk("user_id", "users", "SET NULL"),
        sa.Index("ix_audit_logs_user_id", "user_id"),
        sa.Index("ix_audit_logs_entity_type", "entity_type"),
        sa.Index("ix_audit_logs_entity_id", "entity_id"),
        sa.Index("ix_audit_logs_action", "action"),
        sa.Index("ix_audit_logs_created_at", "created_at"),
        **TABLE_KWARGS,
    )


def downgrade():
    for table_name in (
        "audit_logs",
        "candidates",
        "job_openings",
        "announcements",
        "performance_reviews",
        "employee_salary_components",
        "salary_components",
        "payrolls",
        "payroll_periods",
        "holidays",
        "leave_requests",
        "leave_types",
        "attendance",
        "employee_documents",
    ):
        op.drop_table(table_name)

    op.drop_constraint("fk_departments_manager_employee_id", "departments", type_="foreignkey")
    op.drop_table("employees")
    op.drop_table("positions")
    op.drop_table("departments")
    op.drop_table("users")
    op.drop_table("roles")
