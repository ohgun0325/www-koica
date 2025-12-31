'use client';

import { useEffect, useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';

export default function OAuthCallback() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('');

  useEffect(() => {
    const accessToken = searchParams.get('accessToken');
    const refreshToken = searchParams.get('refreshToken');
    const provider = searchParams.get('provider');
    const success = searchParams.get('success');

    if (success === 'true' && accessToken) {
      // 토큰을 localStorage에 저장
      localStorage.setItem('accessToken', accessToken);
      if (refreshToken) {
        localStorage.setItem('refreshToken', refreshToken);
      }
      
      // storage 이벤트 발생 (다른 탭/창에서 로그인 상태 동기화)
      window.dispatchEvent(new Event('storage'));
      
      setStatus('success');
      setMessage(`${provider || '네이버'} 로그인에 성공했습니다!`);
      
      // 2초 후 메인 페이지로 리다이렉트
      setTimeout(() => {
        router.push('/');
      }, 2000);
    } else {
      setStatus('error');
      setMessage('로그인에 실패했습니다.');
    }
  }, [searchParams, router]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-blue-100 to-white flex items-center justify-center">
      <div className="text-center">
        {status === 'loading' && (
          <div className="space-y-4">
            <div className="w-16 h-16 border-4 border-[#003478] border-t-transparent rounded-full animate-spin mx-auto"></div>
            <p className="text-gray-600">로그인 처리 중...</p>
          </div>
        )}
        {status === 'success' && (
          <div className="space-y-4">
            <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto">
              <svg
                className="w-8 h-8 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M5 13l4 4L19 7"
                />
              </svg>
            </div>
            <p className="text-lg font-semibold text-gray-800">{message}</p>
            <p className="text-sm text-gray-500">잠시 후 메인 페이지로 이동합니다...</p>
          </div>
        )}
        {status === 'error' && (
          <div className="space-y-4">
            <div className="w-16 h-16 bg-red-500 rounded-full flex items-center justify-center mx-auto">
              <svg
                className="w-8 h-8 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </div>
            <p className="text-lg font-semibold text-gray-800">{message}</p>
            <button
              onClick={() => router.push('/')}
              className="px-6 py-2 bg-[#003478] text-white rounded-lg hover:bg-[#002a5c] transition-colors"
            >
              메인으로 돌아가기
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

