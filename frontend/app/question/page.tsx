'use client';

import { questions } from '@/mock_data/question';
import type { Question } from '@/types/question';
import { useEffect, useState } from 'react';
import { Questions } from './questions';

export default function Home() {
  const [questionsData, setQuestionsData] = useState<Question[]>(questions);

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const response = await fetch('/api/questions');
        if (response.ok) {
          const data: Question[] = await response.json();
          setQuestionsData(data);
        } else {
          console.warn('Failed to fetch questions from API, using mock data');
        }
      } catch (error) {
        console.error('Error fetching questions:', error);
        console.warn('Using mock data as fallback');
      }
    };

    fetchQuestions();
  }, []);

  return (
    <main className='py-5 px-5'>
      <h1 className='text-pink-700 font-bold text-2xl'>
        あなたの希望職種と
        <br />
        これまでの経歴を教えて下さい！
      </h1>
      <Questions questions={questionsData} />
    </main>
  );
}
