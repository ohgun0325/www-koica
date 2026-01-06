import { create } from 'zustand';

interface UserInfo {
  email?: string;
  name?: string;
}

interface AuthState {
  // Access Token은 메모리에만 보관 (짧은 만료 시간: 5~15분)
  accessToken: string | null;
  
  // Refresh Token은 httpOnly 쿠키에 저장되어야 하지만,
  // 클라이언트에서 관리가 필요한 경우를 위해 포함
  refreshToken: string | null;
  
  // 사용자 정보
  userInfo: UserInfo | null;
  
  // 로그인 여부
  isLoggedIn: boolean;
  
  // Actions
  setAccessToken: (token: string | null) => void;
  setRefreshToken: (token: string | null) => void;
  setUserInfo: (info: UserInfo | null) => void;
  login: (accessToken: string, refreshToken: string | null, userInfo: UserInfo | null) => void;
  logout: () => void;
}

/**
 * 인증 상태 관리 스토어
 * 
 * 보안 원칙:
 * - Access Token: 메모리(Zustand)에만 저장, localStorage 사용 금지
 * - Refresh Token: httpOnly 쿠키 권장, 클라이언트 저장 시 XSS 위험
 * - 페이지 새로고침 시 토큰 소실 → Refresh Token으로 재발급 로직 필요
 */
export const useAuthStore = create<AuthState>((set) => ({
  accessToken: null,
  refreshToken: null,
  userInfo: null,
  isLoggedIn: false,

  setAccessToken: (token) => 
    set({ 
      accessToken: token,
      isLoggedIn: !!token 
    }),

  setRefreshToken: (token) => 
    set({ refreshToken: token }),

  setUserInfo: (info) => 
    set({ userInfo: info }),

  login: (accessToken, refreshToken, userInfo) => {
    // JWT 토큰 파싱하여 사용자 정보 추출
    try {
      let parsedUserInfo = userInfo;
      
      // userInfo가 제공되지 않았다면 accessToken에서 추출 시도
      if (!userInfo && accessToken) {
        const payload = JSON.parse(atob(accessToken.split('.')[1]));
        parsedUserInfo = {
          email: payload.email,
          name: payload.name,
        };
      }

      set({
        accessToken,
        refreshToken,
        userInfo: parsedUserInfo,
        isLoggedIn: true,
      });
    } catch (e) {
      console.error('Failed to parse token:', e);
      set({
        accessToken,
        refreshToken,
        userInfo,
        isLoggedIn: true,
      });
    }
  },

  logout: () => 
    set({
      accessToken: null,
      refreshToken: null,
      userInfo: null,
      isLoggedIn: false,
    }),
}));

