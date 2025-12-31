'use client';

import { X } from 'lucide-react';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
  activeSection: 'notice' | 'news' | null;
  onSectionChange: (section: 'notice' | 'news' | null) => void;
}

// 공지사항 샘플 데이터
const notices = [
  { id: 1, title: '2024년 KOICA 사업 안내', date: '2024-01-15' },
  { id: 2, title: '신규 프로젝트 지원 모집 공고', date: '2024-01-10' },
  { id: 3, title: '시스템 점검 안내', date: '2024-01-05' },
  { id: 4, title: '연말연시 휴무 안내', date: '2023-12-20' },
  { id: 5, title: '2024년도 예산 배정 공지', date: '2023-12-15' },
];

// 뉴스룸 샘플 데이터
const news = [
  { id: 1, title: 'KOICA, 아프리카 개발협력 프로젝트 성과 발표', date: '2024-01-20' },
  { id: 2, title: '한-아세안 협력사업 확대 협약 체결', date: '2024-01-18' },
  { id: 3, title: '글로벌 보건의료 지원 프로그램 시작', date: '2024-01-12' },
  { id: 4, title: '교육 인프라 구축 사업 완료 보고', date: '2024-01-08' },
  { id: 5, title: '기후변화 대응 프로젝트 성과 공유회 개최', date: '2024-01-03' },
];

export default function Sidebar({ isOpen, onClose, activeSection, onSectionChange }: SidebarProps) {
  const handleSectionClick = (section: 'notice' | 'news') => {
    if (activeSection === section) {
      onSectionChange(null);
    } else {
      onSectionChange(section);
    }
  };

  return (
    <>
      {/* Backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 transition-opacity"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <div
        className={`fixed top-0 left-0 h-full w-80 bg-white shadow-2xl z-50 transform transition-transform duration-300 ease-in-out ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          <h2 className="text-lg font-bold text-[#003478]">메뉴</h2>
          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
            aria-label="닫기"
          >
            <X className="w-5 h-5 text-gray-600" />
          </button>
        </div>

        {/* Menu Items */}
        <div className="p-4 space-y-2">
          {/* 공지사항 버튼 */}
          <button
            onClick={() => handleSectionClick('notice')}
            className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
              activeSection === 'notice'
                ? 'bg-[#003478] text-white'
                : 'bg-gray-50 text-gray-700 hover:bg-gray-100'
            }`}
          >
            <span className="font-medium">공지사항</span>
          </button>

          {/* 뉴스룸 버튼 */}
          <button
            onClick={() => handleSectionClick('news')}
            className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
              activeSection === 'news'
                ? 'bg-[#003478] text-white'
                : 'bg-gray-50 text-gray-700 hover:bg-gray-100'
            }`}
          >
            <span className="font-medium">뉴스룸</span>
          </button>
        </div>

        {/* Content Area */}
        {activeSection && (
          <div className="border-t border-gray-200 p-4 overflow-y-auto" style={{ maxHeight: 'calc(100vh - 200px)' }}>
            <h3 className="text-md font-semibold text-[#003478] mb-4">
              {activeSection === 'notice' ? '공지사항' : '뉴스룸'}
            </h3>
            <div className="space-y-3">
              {(activeSection === 'notice' ? notices : news).map((item) => (
                <div
                  key={item.id}
                  className="p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer border border-gray-200"
                >
                  <p className="font-medium text-gray-800 mb-1">{item.title}</p>
                  <p className="text-xs text-gray-500">{item.date}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </>
  );
}

