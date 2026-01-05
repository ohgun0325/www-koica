'use client';

import { useState, useCallback, useRef } from 'react';
import { Upload, X, FileText, CheckCircle2, Download } from 'lucide-react';
import Header from '@/components/Header';
import MainNavigation from '@/components/MainNavigation';
import Footer from '@/components/Footer';
import LoginModal from '@/components/LoginModal';
import { createMainHandlers } from '@/services/mainservice';

interface UploadedFile {
  id: string;
  file: File;
  status: 'uploading' | 'success' | 'error';
  progress: number;
  thumbnail?: string; // 파일 썸네일 URL
  originalFilename?: string; // 서버에 저장된 파일명
}

export default function NewsPage() {
  const [activeMainTab, setActiveMainTab] = useState('news');
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const pdfjsInitialized = useRef(false);

  const { handleLoginClick, handleLoginRequired, handleLogin } = 
    createMainHandlers(setIsLoginModalOpen);

  const handleDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = Array.from(e.dataTransfer.files);
    handleFiles(files);
  }, []);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const files = Array.from(e.target.files);
      handleFiles(files);
    }
  }, []);

  const generateThumbnail = (file: File): Promise<string | undefined> => {
    return new Promise((resolve) => {
      // 브라우저 환경이 아니면 썸네일 생성 안 함
      if (typeof window === 'undefined') {
        resolve(undefined);
        return;
      }

      // 이미지 파일인 경우
      if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => {
          resolve(e.target?.result as string);
        };
        reader.onerror = () => resolve(undefined);
        reader.readAsDataURL(file);
      }
      // PDF 파일인 경우 - PDF.js를 사용하여 첫 페이지를 썸네일로 생성
      else if (file.type === 'application/pdf') {
        const reader = new FileReader();
        reader.onload = async (e) => {
          // 브라우저 환경 확인
          if (typeof window === 'undefined') {
            resolve(undefined);
            return;
          }

          try {
            // 동적 import로 PDF.js 로드 (클라이언트 사이드에서만)
            // Next.js에서 PDF.js를 안전하게 로드하기 위해 default export 확인
            const pdfjsModule = await import('pdfjs-dist');
            const pdfjsLib = pdfjsModule.default || pdfjsModule;
            
            // 모듈이 제대로 로드되지 않은 경우
            if (!pdfjsLib || typeof pdfjsLib !== 'object') {
              resolve(undefined);
              return;
            }
            
            // Worker 경로 설정 (한 번만 초기화)
            if (!pdfjsInitialized.current && pdfjsLib.GlobalWorkerOptions) {
              const version = pdfjsLib.version || '3.11.174';
              pdfjsLib.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${version}/pdf.worker.min.js`;
              pdfjsInitialized.current = true;
            }
            
            // getDocument 함수 확인
            const getDocument = pdfjsLib.getDocument;
            if (!getDocument || typeof getDocument !== 'function') {
              resolve(undefined);
              return;
            }
            
            const arrayBuffer = e.target?.result as ArrayBuffer;
            if (!arrayBuffer) {
              resolve(undefined);
              return;
            }

            const pdf = await getDocument({ 
              data: arrayBuffer,
              useSystemFonts: true,
            }).promise;
            
            const page = await pdf.getPage(1);
            
            const viewport = page.getViewport({ scale: 0.5 });
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');
            
            if (!context) {
              resolve(undefined);
              return;
            }
            
            canvas.height = viewport.height;
            canvas.width = viewport.width;
            
            await page.render({
              canvasContext: context,
              viewport: viewport,
            }).promise;
            
            resolve(canvas.toDataURL());
          } catch (error) {
            // 에러를 조용히 처리 (콘솔에만 로그)
            if (process.env.NODE_ENV === 'development') {
              console.warn('PDF 썸네일 생성 실패:', error);
            }
            // PDF.js가 없거나 실패한 경우 undefined 반환 (아이콘 표시)
            resolve(undefined);
          }
        };
        reader.onerror = () => resolve(undefined);
        reader.readAsArrayBuffer(file);
      }
      // 기타 파일은 썸네일 없음
      else {
        resolve(undefined);
      }
    });
  };

  const uploadFileToServer = async (file: File, mode: 'detection' | 'pose' = 'pose'): Promise<{ yoloResultUrl: string; filename: string } | string | null> => {
    try {
      // 이미지 파일만 업로드
      if (!file.type.startsWith('image/')) {
        return null;
      }

      const formData = new FormData();
      formData.append('file', file);

      // cv.ohgun.site API로 업로드
      const response = await fetch(`http://localhost:8000/api/upload?mode=${mode}`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || '업로드 실패');
      }

      const result = await response.json();
      console.log('업로드 성공:', result);
      console.log('YOLO 결과 URL:', result.yolo_result_url);
      
      // YOLO 결과 이미지 URL 반환 (파일명도 함께 저장)
      if (result.yolo_result_url) {
        console.log('YOLO 결과 URL 반환:', result.yolo_result_url);
        // 파일명 정보를 함께 반환하기 위해 객체로 변경
        return {
          yoloResultUrl: result.yolo_result_url,
          filename: result.filename
        };
      }
      
      console.warn('YOLO 결과 URL이 없습니다.');
      return null;
    } catch (error) {
      console.error('업로드 오류:', error);
      return null;
    }
  };

  const handleFiles = async (files: File[]) => {
    const newFiles: UploadedFile[] = files.map((file) => {
      // 초기에는 썸네일 없음 (업로드 후 YOLO 결과로 업데이트)
      return {
        id: Math.random().toString(36).substring(7),
        file,
        status: 'uploading' as const,
        progress: 0,
        thumbnail: undefined,
      };
    });

    setUploadedFiles((prev) => [...prev, ...newFiles]);

    // 실제 파일 업로드 및 진행률 업데이트
    newFiles.forEach(async (fileItem) => {
      // 업로드 시작
      let progress = 0;
      const progressInterval = setInterval(() => {
        progress += 20;
        if (progress < 90) {
          setUploadedFiles((prev) =>
            prev.map((item) =>
              item.id === fileItem.id
                ? { ...item, progress: Math.min(progress, 90) }
                : item
            )
          );
        }
      }, 100);

      // 실제 업로드
      const uploadResult = await uploadFileToServer(fileItem.file);
      
      clearInterval(progressInterval);
      
      // 업로드 완료 및 썸네일 업데이트
      console.log('업로드 완료. YOLO 결과:', uploadResult);
      
      if (uploadResult && typeof uploadResult === 'object' && uploadResult.yoloResultUrl) {
        // YOLO 결과 이미지 URL로 썸네일 설정
        const fullUrl = `http://localhost:8000${uploadResult.yoloResultUrl}`;
        console.log('썸네일 URL 설정:', fullUrl);
        
        setUploadedFiles((prev) =>
          prev.map((item) => {
            if (item.id === fileItem.id) {
              console.log('썸네일 업데이트:', item.id, fullUrl);
              return { 
                ...item, 
                progress: 100,
                status: 'success' as const,
                thumbnail: fullUrl,
                originalFilename: uploadResult.filename
              };
            }
            return item;
          })
        );
      } else if (uploadResult && typeof uploadResult === 'string') {
        // 이전 형식 호환성 유지
        const fullUrl = `http://localhost:8000${uploadResult}`;
        setUploadedFiles((prev) =>
          prev.map((item) => {
            if (item.id === fileItem.id) {
              return { 
                ...item, 
                progress: 100,
                status: 'success' as const,
                thumbnail: fullUrl
              };
            }
            return item;
          })
        );
      } else {
        console.warn('YOLO 결과 URL이 없어 원본 썸네일 사용');
        // 실패 시 원본 이미지 썸네일 사용
        const thumbnail = await generateThumbnail(fileItem.file);
        setUploadedFiles((prev) =>
          prev.map((item) =>
            item.id === fileItem.id
              ? { 
                  ...item, 
                  progress: 100,
                  status: 'error' as const,
                  thumbnail: thumbnail
                }
              : item
          )
        );
      }
    });
  };

  const simulateUpload = (fileId: string) => {
    let progress = 0;
    const interval = setInterval(() => {
      progress += 10;
      setUploadedFiles((prev) =>
        prev.map((item) =>
          item.id === fileId
            ? { ...item, progress: Math.min(progress, 100) }
            : item
        )
      );

      if (progress >= 100) {
        clearInterval(interval);
        setUploadedFiles((prev) =>
          prev.map((item) =>
            item.id === fileId ? { ...item, status: 'success' as const } : item
          )
        );
      }
    }, 200);
  };

  const removeFile = (fileId: string) => {
    setUploadedFiles((prev) => prev.filter((item) => item.id !== fileId));
  };

  const downloadFace = async (filename: string, faceIndex: number = 0) => {
    try {
      console.log('얼굴 다운로드 요청:', filename, faceIndex);
      const response = await fetch(
        `http://localhost:8000/api/upload/face-crop/${encodeURIComponent(filename)}?face_index=${faceIndex}`,
        {
          method: 'GET',
        }
      );

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: '얼굴 다운로드 실패' }));
        console.error('얼굴 다운로드 오류:', errorData);
        throw new Error(errorData.detail || '얼굴 다운로드 실패');
      }

      // 파일 다운로드
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `face_${faceIndex + 1}_${filename}`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('얼굴 다운로드 오류:', error);
      alert('얼굴 다운로드 중 오류가 발생했습니다.');
    }
  };

  return (
    <div className="min-h-screen bg-white">
      <Header onLoginClick={handleLoginClick} />
      <MainNavigation
        activeTab={activeMainTab}
        setActiveTab={setActiveMainTab}
        onLoginRequired={handleLoginRequired}
      />

      <div className="pt-[180px] pb-20 px-8">
        <div className="max-w-4xl mx-auto">
          {/* Header Section */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-[#1a2332] mb-2">ESG 소식</h1>
            <p className="text-gray-600">파일을 드래그 앤 드롭하여 업로드하세요</p>
          </div>

          {/* Drag and Drop Zone */}
          <div
            onDragEnter={handleDragEnter}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            className={`relative border-2 border-dashed rounded-2xl p-12 text-center transition-all ${
              isDragging
                ? 'border-[#0D4ABB] bg-[#0D4ABB]/5 scale-[1.02]'
                : 'border-gray-300 bg-gray-50 hover:border-[#0D4ABB]/50 hover:bg-gray-100'
            }`}
          >
            <input
              type="file"
              id="file-upload"
              className="hidden"
              multiple
              onChange={handleFileInput}
            />
            <label
              htmlFor="file-upload"
              className="cursor-pointer flex flex-col items-center gap-4"
            >
              <div className={`w-20 h-20 rounded-full flex items-center justify-center transition-all ${
                isDragging
                  ? 'bg-[#0D4ABB] text-white scale-110'
                  : 'bg-[#0D4ABB]/10 text-[#0D4ABB]'
              }`}>
                <Upload className="w-10 h-10" />
              </div>
              <div>
                <p className="text-xl font-semibold text-[#1a2332] mb-2">
                  {isDragging ? '파일을 여기에 놓으세요' : '파일을 드래그하거나 클릭하여 업로드'}
                </p>
                <p className="text-gray-500 text-sm">
                  PDF, DOCX, XLSX 파일을 지원합니다
                </p>
              </div>
            </label>
          </div>

          {/* Uploaded Files List */}
          {uploadedFiles.length > 0 && (
            <div className="mt-8 space-y-4">
              <h2 className="text-xl font-semibold text-[#1a2332]">업로드된 파일</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {uploadedFiles.map((fileItem) => (
                  <div
                    key={fileItem.id}
                    className="bg-white border border-gray-200 rounded-xl hover:shadow-md transition-all overflow-hidden"
                  >
                    {/* 파일 썸네일/표지 */}
                    <div className="relative w-full aspect-[4/3] bg-gray-100 flex items-center justify-center overflow-hidden">
                      {fileItem.thumbnail ? (
                        <img
                          src={fileItem.thumbnail}
                          alt={fileItem.file.name}
                          className="w-full h-full object-cover"
                        />
                      ) : (
                        <FileText className="w-16 h-16 text-gray-400" />
                      )}
                      {fileItem.status === 'uploading' && (
                        <div className="absolute inset-0 bg-black/20 flex items-center justify-center">
                          <div className="w-3/4 bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-[#0D4ABB] h-2 rounded-full transition-all duration-300"
                              style={{ width: `${fileItem.progress}%` }}
                            />
                          </div>
                        </div>
                      )}
                      {fileItem.status === 'success' && (
                        <div className="absolute top-2 right-2">
                          <CheckCircle2 className="w-6 h-6 text-green-500 bg-white rounded-full" />
                        </div>
                      )}
                      <button
                        onClick={() => removeFile(fileItem.id)}
                        className="absolute top-2 left-2 p-1.5 bg-white/90 hover:bg-white rounded-full transition-colors shadow-sm"
                      >
                        <X className="w-4 h-4 text-gray-600" />
                      </button>
                    </div>
                    {/* 파일 정보 */}
                    <div className="p-4">
                      <p className="font-medium text-[#1a2332] truncate mb-1">
                        {fileItem.file.name}
                      </p>
                      <p className="text-sm text-gray-500 mb-2">
                        {(fileItem.file.size / 1024 / 1024).toFixed(2)} MB
                      </p>
                      {fileItem.status === 'success' && fileItem.originalFilename && (
                        <button
                          onClick={() => downloadFace(fileItem.originalFilename!, 0)}
                          className="w-full flex items-center justify-center gap-2 px-3 py-2 bg-[#0D4ABB] text-white rounded-lg hover:bg-[#0D4ABB]/90 transition-colors text-sm font-medium"
                        >
                          <Download className="w-4 h-4" />
                          얼굴 다운로드
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      <Footer />

      <LoginModal
        isOpen={isLoginModalOpen}
        onClose={() => setIsLoginModalOpen(false)}
        onNaverLogin={handleLogin}
      />
    </div>
  );
}

