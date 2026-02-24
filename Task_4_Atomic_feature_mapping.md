ASSETTRACK PRO – ATOMIC FEATURE LIST, API & DATABASE MAPPING
Prepared By: Keerthana M

MODULE: Authentication & Access Control
Feature: Admin Login
API Endpoint: POST /api/auth/login
Database Action: SELECT * FROM admins WHERE admin_email = ?

Feature: Admin Logout
API Endpoint: POST /api/auth/logout
Database Action: No database change (invalidate JWT on client/server)

Feature: Create New Admin
API Endpoint: POST /api/admins
Database Action: INSERT into admins table

Feature: View All Admins
API Endpoint: GET /api/admins
Database Action: SELECT * FROM admins

MODULE: Department Management
Feature: Add Department
API Endpoint: POST /api/departments
Database Action: INSERT into departments table

Feature: View All Departments
API Endpoint: GET /api/departments
Database Action: SELECT * FROM departments

Feature: Update Department
API Endpoint: PUT /api/departments/:id
Database Action: UPDATE departments SET department_name = ? WHERE department_id = ?

Feature: Delete Department
API Endpoint: DELETE /api/departments/:id
Database Action: DELETE FROM departments WHERE department_id = ?


MODULE: Employee Management

Feature: Add New Employee
API Endpoint: POST /api/employees
Database Action: INSERT into employees table (set status = 'ACTIVE')

Feature: View All Employees
API Endpoint: GET /api/employees
Database Action: SELECT * FROM employees

Feature: Update Employee Details
API Endpoint: PUT /api/employees/:id
Database Action: UPDATE employees SET fields = new values WHERE employee_id = ?

Feature: Deactivate Employee
API Endpoint: PATCH /api/employees/:id/deactivate
Database Action: UPDATE employees SET status = 'INACTIVE' WHERE employee_id = ?

Feature: View Assets Assigned to Employee
API Endpoint: GET /api/employees/:id/assets
Database Action: SELECT * FROM asset_assignments WHERE employee_id = ? AND assignment_status = 'ASSIGNED'


MODULE: Asset Category Management

Feature: Add Asset Category
API Endpoint: POST /api/categories
Database Action: INSERT into asset_categories table

Feature: View All Categories
API Endpoint: GET /api/categories
Database Action: SELECT * FROM asset_categories

Feature: Update Category
API Endpoint: PUT /api/categories/:id
Database Action: UPDATE asset_categories SET category_name = ? WHERE category_id = ?

Feature: Delete Category
API Endpoint: DELETE /api/categories/:id
Database Action: DELETE FROM asset_categories WHERE category_id = ?


MODULE: Asset Management

Feature: Add New Asset
API Endpoint: POST /api/assets
Database Action: INSERT into assets table (set asset_status = 'AVAILABLE')

Feature: View All Assets
API Endpoint: GET /api/assets
Database Action: SELECT * FROM assets

Feature: View Single Asset
API Endpoint: GET /api/assets/:id
Database Action: SELECT * FROM assets WHERE asset_id = ?

Feature: Update Asset
API Endpoint: PUT /api/assets/:id
Database Action: UPDATE assets SET fields = new values WHERE asset_id = ?

Feature: Archive Asset
API Endpoint: PATCH /api/assets/:id/archive
Database Action: UPDATE assets SET asset_status = 'ARCHIVED' WHERE asset_id = ?

Feature: Restore Archived Asset
API Endpoint: PATCH /api/assets/:id/restore
Database Action: UPDATE assets SET asset_status = 'AVAILABLE' WHERE asset_id = ?

Feature: Mark Asset as Broken
API Endpoint: PATCH /api/assets/:id/mark-broken
Database Action: UPDATE assets SET asset_status = 'BROKEN' WHERE asset_id = ?

Feature: Mark Asset as Lost
API Endpoint: PATCH /api/assets/:id/mark-lost
Database Action: UPDATE assets SET asset_status = 'LOST' WHERE asset_id = ?

Feature: Delete Asset Permanently
API Endpoint: DELETE /api/assets/:id
Database Action: DELETE FROM assets WHERE asset_id = ?

Feature: Search Asset by Tag
API Endpoint: GET /api/assets/search?asset_tag=AST001
Database Action: SELECT * FROM assets WHERE asset_tag = ?

Feature: Filter Assets by Category
API Endpoint: GET /api/assets?category_id=1
Database Action: SELECT * FROM assets WHERE category_id = ?

Feature: Filter Assets by Status
API Endpoint: GET /api/assets?status=AVAILABLE
Database Action: SELECT * FROM assets WHERE asset_status = ?

Feature: Get Asset Count by Status
API Endpoint: GET /api/assets/count-by-status
Database Action: SELECT asset_status, COUNT(*) FROM assets GROUP BY asset_status


MODULE: Asset Assignment

Feature: Assign Asset to Employee
API Endpoint: POST /api/assignments
Database Action:

INSERT into asset_assignments

UPDATE assets SET asset_status = 'ASSIGNED'

INSERT into asset_history (action_type = 'ASSIGNED')

Feature: View All Assignments
API Endpoint: GET /api/assignments
Database Action: SELECT * FROM asset_assignments

Feature: View Assignment Details
API Endpoint: GET /api/assignments/:id
Database Action: SELECT * FROM asset_assignments WHERE assignment_id = ?


MODULE: Asset Return & Condition Tracking

Feature: Return Assigned Asset
API Endpoint: POST /api/returns
Database Action:

INSERT into asset_returns

UPDATE asset_assignments SET assignment_status = 'RETURNED'

UPDATE assets SET asset_status = 'AVAILABLE'

INSERT into asset_history (action_type = 'RETURNED')

Feature: View All Returns
API Endpoint: GET /api/returns
Database Action: SELECT * FROM asset_returns

Feature: Mark Returned Asset Condition
API Endpoint: PATCH /api/returns/:id/condition
Database Action: UPDATE asset_returns SET asset_condition = ? WHERE return_id = ?


MODULE: Maintenance Management

Feature: Schedule Maintenance
API Endpoint: POST /api/maintenance
Database Action: INSERT into asset_maintenance

Feature: View Maintenance Records for Asset
API Endpoint: GET /api/assets/:id/maintenance
Database Action: SELECT * FROM asset_maintenance WHERE asset_id = ?

Feature: Update Maintenance Record
API Endpoint: PUT /api/maintenance/:id
Database Action: UPDATE asset_maintenance SET fields = new values WHERE maintenance_id = ?


MODULE: Asset History Timeline

Feature: View Asset History
API Endpoint: GET /api/assets/:id/history
Database Action: SELECT * FROM asset_history WHERE asset_id = ?


MODULE: Dashboard & Insights

Feature: Get Dashboard Summary
API Endpoint: GET /api/dashboard/summary
Database Action:

SELECT COUNT(*) FROM assets

SELECT COUNT(*) FROM assets WHERE asset_status = 'ASSIGNED'

SELECT COUNT(*) FROM assets WHERE asset_status = 'AVAILABLE'

SELECT COUNT(*) FROM asset_assignments WHERE assignment_status = 'ASSIGNED'

Feature: Get Recently Returned Assets
API Endpoint: GET /api/dashboard/recent-returns
Database Action: SELECT * FROM asset_returns ORDER BY return_date DESC LIMIT 10