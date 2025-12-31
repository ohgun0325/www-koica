export function createMainHandlers(setIsLoginModalOpen: (value: boolean) => void) {
  const handleLoginClick = () => {
    setIsLoginModalOpen(true);
  };

  const handleLoginRequired = () => {
    setIsLoginModalOpen(true);
  };

  const handleExplore = () => {
    // Scroll to features section
    const featuresSection = document.getElementById('features');
    if (featuresSection) {
      featuresSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  /**
   * 소셜 로그인 버튼 클릭 시 동작:
   * 1. oauth-service에 네이버 로그인 URL을 요청
   * 2. 응답으로 받은 URL로 브라우저를 리다이렉트
   *
   * NOTE: 현재는 네이버만 사용하므로 단일 엔드포인트로 호출합니다.
   *       추후 Kakao/Google 추가 시 provider 파라미터를 받을 수 있도록 확장할 수 있습니다.
   */
  const handleLogin = async () => {
    try {
      console.log('Login action triggered');

      const baseUrl =
        process.env.NEXT_PUBLIC_OAUTH_BASE_URL ?? 'http://localhost:8080';

      console.log('Requesting login URL from:', `${baseUrl}/oauth/naver/login-url`);

      const response = await fetch(`${baseUrl}/oauth/naver/login-url`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      console.log('Response status:', response.status);
      console.log('Response ok:', response.ok);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Failed to get login url from oauth-service', {
          status: response.status,
          statusText: response.statusText,
          error: errorText,
        });
        alert(`로그인 URL 요청 실패: ${response.status} ${response.statusText}`);
        return;
      }

      const data = (await response.json()) as { url: string; state?: string };
      console.log('Received login URL:', data.url);

      if (!data.url) {
        console.error('No URL in response:', data);
        alert('로그인 URL을 받지 못했습니다.');
        return;
      }

      // 모달 닫고 네이버 로그인 페이지로 이동
      setIsLoginModalOpen(false);
      console.log('Redirecting to:', data.url);
      window.location.href = data.url;
    } catch (error) {
      console.error('Error while requesting Naver login URL', error);
      alert(`로그인 요청 중 오류가 발생했습니다: ${error instanceof Error ? error.message : String(error)}`);
    }
  };

  return {
    handleLoginClick,
    handleLoginRequired,
    handleExplore,
    handleLogin,
  };
}

