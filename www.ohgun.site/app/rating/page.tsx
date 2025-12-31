'use client';

import { useState } from 'react';
import { Search, ChevronDown, ArrowUp, ArrowDown, Minus, Info } from 'lucide-react';
import Header from '@/components/Header';
import MainNavigation from '@/components/MainNavigation';
import Footer from '@/components/Footer';
import LoginModal from '@/components/LoginModal';
import { createMainHandlers } from '@/services/mainservice';

interface CompanyData {
  id: string;
  name: string;
  industry: string;
  overallRating: string;
  overallTrend: 'up' | 'down' | 'same';
  environmentRating: string;
  environmentTrend: 'up' | 'down' | 'same';
  socialRating: string;
  socialTrend: 'up' | 'down' | 'same';
  governanceRating: string;
  governanceTrend: 'up' | 'down' | 'same';
}

const mockData: CompanyData[] = [
  {
    id: '1',
    name: '테크코프 솔루션',
    industry: '정보기술',
    overallRating: 'A',
    overallTrend: 'up',
    environmentRating: 'A',
    environmentTrend: 'up',
    socialRating: 'B+',
    socialTrend: 'same',
    governanceRating: 'A',
    governanceTrend: 'same',
  },
  {
    id: '2',
    name: '그린에너지',
    industry: '재생에너지',
    overallRating: 'A+',
    overallTrend: 'up',
    environmentRating: 'S',
    environmentTrend: 'down',
    socialRating: 'A',
    socialTrend: 'down',
    governanceRating: 'B+',
    governanceTrend: 'up',
  },
  {
    id: '3',
    name: '글로벌 파이낸스 그룹',
    industry: '금융서비스',
    overallRating: 'B',
    overallTrend: 'down',
    environmentRating: 'C+',
    environmentTrend: 'same',
    socialRating: 'B+',
    socialTrend: 'down',
    governanceRating: 'B+',
    governanceTrend: 'up',
  },
  {
    id: '4',
    name: '메디케어 헬스케어',
    industry: '헬스케어 및 제약',
    overallRating: 'A',
    overallTrend: 'up',
    environmentRating: 'B+',
    environmentTrend: 'same',
    socialRating: 'A+',
    socialTrend: 'up',
    governanceRating: 'A',
    governanceTrend: 'same',
  },
  {
    id: '5',
    name: '오토드라이브 모터스',
    industry: '자동차 제조',
    overallRating: 'B',
    overallTrend: 'down',
    environmentRating: 'B',
    environmentTrend: 'same',
    socialRating: 'C+',
    socialTrend: 'up',
    governanceRating: 'C+',
    governanceTrend: 'same',
  },
  {
    id: '6',
    name: '프레시푸드',
    industry: '식품 및 음료',
    overallRating: 'B+',
    overallTrend: 'same',
    environmentRating: 'B',
    environmentTrend: 'same',
    socialRating: 'A',
    socialTrend: 'same',
    governanceRating: 'B',
    governanceTrend: 'down',
  },
  {
    id: '7',
    name: '빌드라이트 건설',
    industry: '건설 및 엔지니어링',
    overallRating: 'C+',
    overallTrend: 'down',
    environmentRating: 'C',
    environmentTrend: 'same',
    socialRating: 'C+',
    socialTrend: 'same',
    governanceRating: 'C+',
    governanceTrend: 'same',
  },
];

const getRatingColor = (rating: string) => {
  if (rating === 'S') return 'bg-red-100 text-red-800 border-red-200';
  if (rating.startsWith('A')) return 'bg-green-100 text-green-800 border-green-200';
  if (rating.startsWith('B')) return 'bg-blue-100 text-blue-800 border-blue-200';
  if (rating.startsWith('C')) return 'bg-yellow-100 text-yellow-800 border-yellow-200';
  return 'bg-gray-100 text-gray-800 border-gray-200';
};

const getTrendIcon = (trend: 'up' | 'down' | 'same') => {
  if (trend === 'up') return <ArrowUp className="w-4 h-4 text-green-600" />;
  if (trend === 'down') return <ArrowDown className="w-4 h-4 text-red-600" />;
  return <Minus className="w-4 h-4 text-gray-400" />;
};

export default function RatingPage() {
  const [activeMainTab, setActiveMainTab] = useState('rating');
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);
  const [searchInput, setSearchInput] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [evaluationStandard, setEvaluationStandard] = useState<'K-ESG' | 'ESRS'>('K-ESG');
  const [referenceDate, setReferenceDate] = useState('2025년 12월');
  const [isDateDropdownOpen, setIsDateDropdownOpen] = useState(false);

  const { handleLoginClick, handleLoginRequired, handleLogin } = createMainHandlers(setIsLoginModalOpen);

  const months = [
    '2025년 12월',
    '2025년 11월',
    '2025년 10월',
    '2025년 9월',
    '2025년 8월',
    '2025년 7월',
  ];

  const handleSearch = () => {
    setSearchQuery(searchInput);
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const filteredData = mockData.filter((company) =>
    company.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-white">
      <Header onLoginClick={handleLoginClick} />
      <MainNavigation
        activeTab={activeMainTab}
        setActiveTab={setActiveMainTab}
        onLoginRequired={handleLoginRequired}
      />

      <div className="pt-[180px] pb-20 px-8">
        <div className="max-w-[1440px] mx-auto">
          {/* Header Section */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-[#1a2332] mb-2">기업 ESG 등급</h1>
            <p className="text-gray-600">매월 업데이트 · 독립적 지속가능성 평가</p>
          </div>

          {/* Filters Section */}
          <div className="flex items-center gap-4 mb-6 flex-wrap">
            {/* Evaluation Standard Toggle */}
            <div className="flex items-center gap-2 bg-gray-100 rounded-lg p-1">
              <button
                onClick={() => setEvaluationStandard('K-ESG')}
                className={`px-4 py-2 rounded-md transition-all ${
                  evaluationStandard === 'K-ESG'
                    ? 'bg-white text-[#0D4ABB] shadow-sm font-medium'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                K-ESG
              </button>
              <button
                onClick={() => setEvaluationStandard('ESRS')}
                className={`px-4 py-2 rounded-md transition-all ${
                  evaluationStandard === 'ESRS'
                    ? 'bg-white text-[#0D4ABB] shadow-sm font-medium'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                ESRS
              </button>
            </div>

            {/* Reference Date Dropdown */}
            <div className="relative">
              <button
                onClick={() => setIsDateDropdownOpen(!isDateDropdownOpen)}
                className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <span>{referenceDate}</span>
                <ChevronDown className={`w-4 h-4 transition-transform ${isDateDropdownOpen ? 'rotate-180' : ''}`} />
              </button>
              {isDateDropdownOpen && (
                <>
                  <div
                    className="fixed inset-0 z-10"
                    onClick={() => setIsDateDropdownOpen(false)}
                  />
                  <div className="absolute top-full left-0 mt-1 bg-white border border-gray-300 rounded-lg shadow-lg z-20 min-w-[160px]">
                    {months.map((month) => (
                      <button
                        key={month}
                        onClick={() => {
                          setReferenceDate(month);
                          setIsDateDropdownOpen(false);
                        }}
                        className={`w-full text-left px-4 py-2 hover:bg-gray-50 first:rounded-t-lg last:rounded-b-lg ${
                          referenceDate === month ? 'bg-blue-50 text-[#0D4ABB] font-medium' : ''
                        }`}
                      >
                        {month}
                      </button>
                    ))}
                  </div>
                </>
              )}
            </div>
          </div>

          {/* Table Section */}
          <div>
            {/* Search Bar and Rating Guide - Same Row */}
            <div className="mb-4 flex items-start gap-4 flex-wrap">
              {/* Search Bar */}
              <div className="flex items-center gap-3 flex-1 min-w-[300px]">
                <div className="relative flex-1 max-w-md">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="text"
                    placeholder="회사명 검색"
                    value={searchInput}
                    onChange={(e) => setSearchInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    className="w-full pl-10 pr-4 py-2.5 bg-white text-gray-900 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#0D4ABB] focus:border-transparent"
                  />
                </div>
                <button
                  onClick={handleSearch}
                  className="px-6 py-2.5 bg-[#0D4ABB] text-white rounded-lg hover:bg-[#0a3a9b] transition-colors font-medium whitespace-nowrap"
                >
                  조회
                </button>
              </div>

              {/* Rating Guide - Next to Search Bar */}
              <div className="bg-white border border-gray-200 rounded-lg p-2.5 shadow-sm flex-1 min-w-[500px]">
                <div className="flex items-center gap-1.5 mb-1.5">
                  <Info className="w-3.5 h-3.5 text-[#0D4ABB]" />
                  <h3 className="font-semibold text-gray-900 text-sm">평가등급표</h3>
                </div>
                <div className="flex items-center gap-3 flex-wrap text-xs">
                  <div className="flex items-center gap-1.5">
                    <span className="px-1.5 py-0.5 rounded bg-green-100 text-green-800 border border-green-200 font-medium text-[10px]">S</span>
                    <span className="text-gray-600 text-xs">100점</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <span className="px-1.5 py-0.5 rounded bg-green-100 text-green-800 border border-green-200 font-medium text-[10px]">A+</span>
                    <span className="text-gray-600 text-xs">95점 이상</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <span className="px-1.5 py-0.5 rounded bg-green-100 text-green-800 border border-green-200 font-medium text-[10px]">A</span>
                    <span className="text-gray-600 text-xs">90점 이상</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <span className="px-1.5 py-0.5 rounded bg-blue-100 text-blue-800 border border-blue-200 font-medium text-[10px]">B+</span>
                    <span className="text-gray-600 text-xs">85점 이상</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <span className="px-1.5 py-0.5 rounded bg-blue-100 text-blue-800 border border-blue-200 font-medium text-[10px]">B</span>
                    <span className="text-gray-600 text-xs">80점 이상</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <span className="px-1.5 py-0.5 rounded bg-yellow-100 text-yellow-800 border border-yellow-200 font-medium text-[10px]">C+</span>
                    <span className="text-gray-600 text-xs">75점 이상</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <span className="px-1.5 py-0.5 rounded bg-yellow-100 text-yellow-800 border border-yellow-200 font-medium text-[10px]">C</span>
                    <span className="text-gray-600 text-xs">70점 이상</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-[#0D4ABB] text-white">
                    <tr>
                      <th className="px-6 py-4 text-left font-semibold">기업명</th>
                      <th className="px-6 py-4 text-left font-semibold">종합 ESG 등급</th>
                      <th className="px-6 py-4 text-left font-semibold">환경 (E)</th>
                      <th className="px-6 py-4 text-left font-semibold">사회 (S)</th>
                      <th className="px-6 py-4 text-left font-semibold">지배구조 (G)</th>
                    </tr>
                  </thead>
                <tbody>
                  {filteredData.map((company, index) => (
                    <tr
                      key={company.id}
                      className={`border-b border-gray-200 hover:bg-gray-50 transition-colors ${
                        index % 2 === 0 ? 'bg-white' : 'bg-gray-50/50'
                      }`}
                    >
                      <td className="px-6 py-4">
                        <div>
                          <div className="font-medium text-gray-900">{company.name}</div>
                          <div className="text-sm text-gray-500">{company.industry}</div>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2">
                          <span
                            className={`px-3 py-1 rounded-md border font-medium ${getRatingColor(
                              company.overallRating
                            )}`}
                          >
                            {company.overallRating}
                          </span>
                          {getTrendIcon(company.overallTrend)}
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2">
                          <span
                            className={`px-3 py-1 rounded-md border font-medium ${getRatingColor(
                              company.environmentRating
                            )}`}
                          >
                            {company.environmentRating}
                          </span>
                          {getTrendIcon(company.environmentTrend)}
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2">
                          <span
                            className={`px-3 py-1 rounded-md border font-medium ${getRatingColor(
                              company.socialRating
                            )}`}
                          >
                            {company.socialRating}
                          </span>
                          {getTrendIcon(company.socialTrend)}
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2">
                          <span
                            className={`px-3 py-1 rounded-md border font-medium ${getRatingColor(
                              company.governanceRating
                            )}`}
                          >
                            {company.governanceRating}
                          </span>
                          {getTrendIcon(company.governanceTrend)}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              </div>
            </div>
          </div>
        </div>
      </div>

      <Footer />
      <LoginModal
        isOpen={isLoginModalOpen}
        onClose={() => setIsLoginModalOpen(false)}
        onLogin={handleLogin}
      />
    </div>
  );
}

