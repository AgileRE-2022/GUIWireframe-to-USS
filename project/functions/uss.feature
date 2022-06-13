Feature:
	In order to access dashboard page
	As a user
	I want to validate account access

	Scenario: Success Login
		Given im on url "login"
		When I fill in  ""email"" with "some@email.com"
		And I fill in  ""password"" with "rightpassword"
		Then Then I should see "Dashboardddd"

	Scenario: go to Forgot Password
		Given im on url "/login"
		When I press  "[forgot password]"
		Then Then I should see "Enter your email"

