'use client';

import JobCardWrapper from '@/app/job-match/JobCardWrapper';
import { sampleJobs } from '@/mock_data/jobs';
import type { Job } from '@/types/jobs';
import type { SwipeResult } from '@/types/swipe_results';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function Home() {
  const router = useRouter();
  const [jobs, setJobs] = useState<Job[]>([]);
  const [swipeResult, setSwipeResult] = useState<SwipeResult>({
    good: [],
    bad: [],
  });

  useEffect(() => {
    // TODO: data fetch
    const fetchJobs = async () => {
      console.log(sampleJobs);
      return sampleJobs;
    };
    fetchJobs().then(jobs => setJobs(jobs));
  }, []);

  const handleSwipe = (jobId: number, status: 'good' | 'bad') => {
    console.log(jobId, status);
    setSwipeResult(prev => {
      const newSwipeResult = { ...prev };
      newSwipeResult[status] = [...newSwipeResult[status], jobId];
      return newSwipeResult;
    });
  };

  // データの送信
  const handleComplete = (jobId: number, status: 'good' | 'bad') => {
    const finalResult = (() => {
      const newSwipeResult = { ...swipeResult };
      newSwipeResult[status] = [...newSwipeResult[status], jobId];
      return newSwipeResult;
    })();
    console.log(finalResult);
    setTimeout(() => {
      router.push('/job-suggestion');
    }, 3000);
  };

  return (
    <main>
      <JobCardWrapper jobs={jobs} handleSwipe={handleSwipe} handleComplete={handleComplete} />
    </main>
  );
}