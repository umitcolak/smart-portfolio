// login_page.dart
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _identifierController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _confirmPasswordController = TextEditingController();

  bool _isLogin = true;
  bool _isLoading = false;

  void _submit() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isLoading = true);

    if (_isLogin) {
      final identifier = _identifierController.text;
      final password = _passwordController.text;

      final response = await http.post(
        Uri.parse('http://127.0.0.1:8000/login'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'login': identifier, 'password': password}),
      );

      setState(() => _isLoading = false);

      if (response.statusCode == 200) {
        final token = jsonDecode(response.body)['access_token'];
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('token', token);
        if (!mounted) return;
        Navigator.pushReplacementNamed(context, '/main');
      } else {
        _showError('Invalid login. Please try again.');
      }
    } else {
      final username = _identifierController.text;
      final email = _emailController.text;
      final password = _passwordController.text;
      final confirmPassword = _confirmPasswordController.text;

      if (password != confirmPassword) {
        _showError('Passwords do not match');
        setState(() => _isLoading = false);
        return;
      }

      final response = await http.post(
        Uri.parse('http://127.0.0.1:8000/register'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'username': username,
          'email': email,
          'password': password,
        }),
      );

      setState(() => _isLoading = false);

      if (response.statusCode == 200) {
        if (!mounted) return;
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Registration successful! Please login.')),
        );
        setState(() => _isLogin = true);
      } else {
        _showError('Registration failed: ${response.body}');
      }
    }
  }

  void _showError(String message) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(message)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Card(
          margin: const EdgeInsets.all(32),
          elevation: 8,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          child: Padding(
            padding: const EdgeInsets.all(24.0),
            child: Form(
              key: _formKey,
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    _isLogin ? 'Login to Smart Portfolio' : 'Create an Account',
                    style: const TextStyle(fontSize: 24),
                  ),
                  const SizedBox(height: 20),
                  TextFormField(
                    controller: _identifierController,
                    decoration: InputDecoration(
                      labelText: _isLogin ? 'Username or Email' : 'Username',
                      border: const OutlineInputBorder(),
                    ),
                    validator: (value) => value == null || value.isEmpty ? 'This field is required' : null,
                  ),
                  if (!_isLogin) ...[
                    const SizedBox(height: 16),
                    TextFormField(
                      controller: _emailController,
                      decoration: const InputDecoration(
                        labelText: 'Email',
                        border: OutlineInputBorder(),
                      ),
                      validator: (value) => value == null || value.isEmpty ? 'Please enter your email' : null,
                    ),
                  ],
                  const SizedBox(height: 16),
                  TextFormField(
                    controller: _passwordController,
                    obscureText: true,
                    decoration: const InputDecoration(
                      labelText: 'Password',
                      border: OutlineInputBorder(),
                    ),
                    validator: (value) => value == null || value.isEmpty ? 'Please enter your password' : null,
                  ),
                  if (!_isLogin) ...[
                    const SizedBox(height: 16),
                    TextFormField(
                      controller: _confirmPasswordController,
                      obscureText: true,
                      decoration: const InputDecoration(
                        labelText: 'Confirm Password',
                        border: OutlineInputBorder(),
                      ),
                      validator: (value) => value != _passwordController.text ? 'Passwords do not match' : null,
                    ),
                  ],
                  const SizedBox(height: 20),
                  _isLoading
                      ? const CircularProgressIndicator()
                      : ElevatedButton(
                          onPressed: _submit,
                          child: Text(_isLogin ? 'Login' : 'Register'),
                        ),
                  const SizedBox(height: 10),
                  TextButton(
                    onPressed: () {
                      setState(() => _isLogin = !_isLogin);
                    },
                    child: Text(_isLogin ? 'Create an account' : 'Already have an account? Login'),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
