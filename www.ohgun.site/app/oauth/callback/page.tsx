'use client';

import { useEffect, useState, Suspense } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/authStore';
import { storeRefreshTokenInCookie } from '@/services/mainservice';

function OAuthCallbackContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('');
  
  // Zustand 스토어에서 login 함수 가져오기
  const { login } = useAuthStore();

  useEffect(() => {
    const processLogin = async () => {
      const accessToken = searchParams.get('accessToken');
      const refreshToken = searchParams.get('refreshToken');
      const provider = searchParams.get('provider');
      const success = searchParams.get('success');

      if (success === 'true' && accessToken) {
        // 1. Refresh Token을 HttpOnly 쿠키에 저장 (XSS 공격 방지)
        if (refreshToken) {
          const cookieStored = await storeRefreshTokenInCookie(refreshToken);
          if (!cookieStored) {
            console.warn('Failed to store refresh token in cookie, but continuing...');
          }
        }

        // 2. Access Token은 메모리(Zustand)에만 저장
        // Refresh Token은 쿠키에 저장되었으므로 Zustand에는 저장하지 않음
        try {
          const payload = JSON.parse(atob(accessToken.split('.')[1]));
          login(accessToken, null, { // refreshToken을 null로 전달 (쿠키에 저장됨)
            email: payload.email,
            name: payload.name,
          });
        } catch (e) {
          console.error('Failed to parse token:', e);
          // 파싱 실패해도 토큰은 저장
          login(accessToken, null, null);
        }
        
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
    };

    processLogin();
  }, [searchParams, router, login]);

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

export default function OAuthCallback() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-blue-100 to-white flex items-center justify-center">
        <div className="text-center space-y-4">
          <div className="w-16 h-16 border-4 border-[#003478] border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="text-gray-600">로딩 중...</p>
        </div>
      </div>
    }>
      <OAuthCallbackContent />
    </Suspense>
  );
}

