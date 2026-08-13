import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ShieldCheck, BookOpen, Lock } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

const Login = () => {
  const [email, setEmail] = useState('admin@libraai.com');
  const [password, setPassword] = useState('••••••••');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    login(email, password);
    navigate('/admin/data-management');
  };

  return (
    <div className="min-h-screen bg-[#F7F7FA] flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
        <div className="flex justify-center items-center gap-2 mb-2">
          <div className="w-10 h-10 rounded-xl bg-[#6D4AFF] flex items-center justify-center text-white font-bold text-xl shadow-md">
            L
          </div>
          <span className="font-bold text-2xl text-[#17152A] tracking-tight">LibraAI</span>
        </div>
        <h2 className="text-[#747184] text-sm font-medium">Intelligent Library OS</h2>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow-sm border border-[#E8E7EF] sm:rounded-xl sm:px-10">
          <div className="mb-6">
            <h3 className="text-xl font-bold text-[#17152A]">Welcome back</h3>
            <p className="text-sm text-[#747184] mt-1">Sign in to access the LibraAI administration console.</p>
          </div>

          <form className="space-y-5" onSubmit={handleSubmit}>
            <div>
              <label className="block text-sm font-medium text-[#17152A]">Email address</label>
              <div className="mt-1">
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full bg-[#F7F7FA] border border-[#E8E7EF] rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#6D4AFF]"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-[#17152A]">Password</label>
              <div className="mt-1">
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full bg-[#F7F7FA] border border-[#E8E7EF] rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#6D4AFF]"
                />
              </div>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <input
                  id="remember-me"
                  type="checkbox"
                  defaultChecked
                  className="h-4 w-4 text-[#6D4AFF] focus:ring-[#6D4AFF] border-[#E8E7EF] rounded"
                />
                <label htmlFor="remember-me" className="ml-2 block text-sm text-[#747184]">
                  Remember me
                </label>
              </div>

              <div className="text-sm">
                <a href="#" className="font-medium text-[#6D4AFF] hover:underline">
                  Forgot password?
                </a>
              </div>
            </div>

            <div>
              <button
                type="submit"
                className="w-full flex justify-center py-2.5 px-4 border border-transparent rounded-lg text-sm font-medium text-white bg-[#6D4AFF] hover:bg-[#5427E6] transition-colors"
              >
                Sign In
              </button>
            </div>
          </form>

          <div className="mt-6 border-t border-[#E8E7EF] pt-4 text-center">
            <div className="inline-flex items-center gap-1.5 text-xs text-[#747184]">
              <ShieldCheck className="w-4 h-4 text-[#16A34A]" />
              Secure administrator access
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
