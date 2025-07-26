'use client';
import type { Job } from '@/types/jobs';
import { createRef, useEffect, useMemo, useRef, useState } from 'react';
import TinderCard from 'react-tinder-card';
import JobCard from './JobCard';

interface JobCardWrapperProps {
  jobs: Job[];
  handleSwipe: (jobId: number, status: 'good' | 'bad') => void;
  handleComplete: (jobId: number, status: 'good' | 'bad') => void;
}

export default function JobCardWrapper({
  jobs,
  handleSwipe,
  handleComplete,
}: JobCardWrapperProps) {
  const [currentIndex, setCurrentIndex] = useState(0);

  const currentIndexRef = useRef(currentIndex);
  const childRefs = useMemo(
    () =>
      Array(jobs.length)
        .fill(0)
        .map(() => createRef<any>()),
    [jobs.length]
  );

  // ページ全体の横スクロール防止
  useEffect(() => {
    document.body.style.overflowX = 'hidden';
    document.documentElement.style.overflowX = 'hidden';

    return () => {
      document.body.style.overflowX = '';
      document.documentElement.style.overflowX = '';
    };
  }, []);

  useEffect(() => {
    setCurrentIndex(jobs.length - 1);
  }, [jobs]);

  // カードのインデックスを更新する関数
  const updateCurrentIndex = (val: number) => {
    setCurrentIndex(val);
    currentIndexRef.current = val;
  };

  const canGoBack = currentIndex < jobs.length - 1;
  const canSwipe = currentIndex >= 0;

  // スワイプ時の処理
  const swiped = (direction: 'left' | 'right', index: number) => {
    const status = direction === 'left' ? 'bad' : 'good';
    updateCurrentIndex(index - 1);
    handleSwipe(jobs[index].id, status);
    if (index - 1 < 0) {
      handleComplete(jobs[index].id, status);
    }
  }

  const outOfFrame = (idx: number) => {
    currentIndexRef.current >= idx && childRefs[idx].current?.restoreCard();
  }

  // スワイプボタンを押したらカードをスワイプする関数
  const swipe = async (dir: 'left' | 'right') => {
    if (canSwipe && currentIndex < jobs.length) {
      await childRefs[currentIndex].current?.swipe(dir);
    }
  };

  // 戻るボタンを押したらカードを復元する関数
  const goBack = async () => {
    if (!canGoBack) return;
    const newIndex = currentIndex + 1;
    updateCurrentIndex(newIndex);
    await childRefs[newIndex].current?.restoreCard();
  };

  return (
    <div
      className="w-full min-h-screen flex flex-col"
      style={{
        overflowX: 'hidden',
        touchAction: 'pan-y pinch-zoom',
        maxWidth: '100vw'
      }}
    >
      <div
        className="flex-shrink-0 px-4"
        style={{ touchAction: 'auto', pointerEvents: 'auto' }}
      >
        <h2 className="text-center text-xl sm:text-2xl font-bold my-3 sm:my-5">
          あなたにおすすめのお仕事
        </h2>
        <p className='text-center text-sm sm:text-base mb-4'>
          直感的に気に入ったら右へスワイプ
        </p>

        {/* プログレスバー */}
        <div className="max-w-md mx-auto mb-4">
          <div className="flex justify-between text-xs sm:text-sm text-gray-600 mb-2">
            <span>進捗状況</span>
            <span>{jobs.length - currentIndex - 1} / {jobs.length}</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2 sm:h-3">
            <div
              className="bg-gradient-to-r from-blue-500 to-purple-600 h-2 sm:h-3 rounded-full transition-all duration-300 ease-out"
              style={{
                width: `${((jobs.length - currentIndex - 1) / jobs.length) * 100}%`
              }}
            ></div>
          </div>
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>開始</span>
            <span>完了</span>
          </div>
        </div>
      </div>

      {currentIndex >= 0 && (
        <div
          className="flex-1 flex justify-center items-center relative px-4 py-8"
          style={{
            overflowX: 'hidden'
          }}
        >
          <div
            className="relative"
            style={{
              width: 'min(350px, calc(100vw - 2rem))',
              height: 'min(70vh, 600px)',
              overflowX: 'hidden'
            }}
          >
            {jobs.map((job, index) => (
              <TinderCard
                ref={childRefs[index]}
                key={job.id}
                onSwipe={(dir) => swiped(dir as 'left' | 'right', index)}
                onCardLeftScreen={() => outOfFrame(index)}
                className="absolute"
                preventSwipe={['up', 'down']}
                swipeRequirementType="position"
                swipeThreshold={80}
              >
                <div
                  className="cursor-grab active:cursor-grabbing"
                  style={{
                    width: 'min(350px, calc(100vw - 2rem))',
                    height: 'min(70vh, 600px)',
                    zIndex: jobs.length - index,
                    transform: index <= currentIndex
                      ? `scale(${1 - (currentIndex - index) * 0.05}) translateY(${(currentIndex - index) * -10}px)`
                      : 'scale(0) translateY(0px)',
                    overflowX: 'hidden',
                    position: 'relative'
                  }}
                >
                  <JobCard key={job.id} job={job} />
                </div>
              </TinderCard>
            ))}
          </div>
        </div>
      )}

      {currentIndex >= 0 && (
        <div
          className="flex-shrink-0 px-4 pb-8"
          style={{
            touchAction: 'auto',
            pointerEvents: 'auto'
          }}
        >
          <div className="flex justify-center gap-2 sm:gap-4 max-w-md mx-auto">
            <button
              onClick={() => swipe('left')}
              disabled={!canSwipe}
              className={`flex-1 sm:flex-none sm:px-6 py-2 sm:py-3 rounded-lg font-semibold text-sm sm:text-base transition-colors ${!canSwipe
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-red-500 text-white hover:bg-red-600 active:bg-red-700'
                }`}
              type="button"
            >
              興味なし
            </button>
            <button
              onClick={() => goBack()}
              disabled={!canGoBack}
              className={`flex-1 sm:flex-none sm:px-6 py-2 sm:py-3 rounded-lg font-semibold text-sm sm:text-base transition-colors ${!canGoBack
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-yellow-500 text-white hover:bg-yellow-600 active:bg-yellow-700'
                }`}
              type="button"
            >
              戻る
            </button>
            <button
              onClick={() => swipe('right')}
              disabled={!canSwipe}
              className={`flex-1 sm:flex-none sm:px-6 py-2 sm:py-3 rounded-lg font-semibold text-sm sm:text-base transition-colors ${!canSwipe
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-green-500 text-white hover:bg-green-600 active:bg-green-700'
                }`}
              type="button"
            >
              興味あり
            </button>
          </div>
        </div>
      )}

      <div
        className={`text-center pb-8 ${currentIndex < 0 ? 'flex-1 flex items-center justify-center' : ''}`}
        style={{ pointerEvents: 'auto' }}
      >
        {currentIndex < 0 && (
          <div className="max-w-md mx-auto px-4">
            <div className="bg-gradient-to-r from-green-50 to-blue-50 border border-green-200 rounded-xl p-8 shadow-lg">
              <div className="text-6xl mb-4">🎉</div>
              <h3 className="text-xl sm:text-2xl font-bold text-gray-800 mb-3">
                お疲れさまでした！
              </h3>
              <p className="text-base sm:text-lg text-gray-700 mb-6">
                全てのお仕事カードの確認が完了しました。
              </p>
              <div className="bg-white rounded-lg p-4 border border-gray-200">
                <p className="text-sm sm:text-base text-gray-600">
                  システムがあなたに合う求人を探しています...
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}