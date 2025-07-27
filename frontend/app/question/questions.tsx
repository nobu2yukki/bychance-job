'use client';

import type { Question } from '@/types/question';
import { useRouter } from 'next/navigation';
import { useState } from 'react';

type Props = {
  questions: Question[];
};

export const Questions = ({ questions }: Props) => {
  const router = useRouter();
  //下、numberからstringへ
  const [answers, setAnswers] = useState<Record<string, string | string[]>>({});
  //下、numberからstringへ
  const handleSingleChoice = (questionId: string, value: string) => {
    setAnswers(prev => ({ ...prev, [questionId]: value }));
    console.log(answers);
  };
  //下、numberからstringへ
  const handleMultiChoice = (questionId: string, value: string) => {
    setAnswers(prev => {
      const current = (prev[questionId] as string[]) || [];
      const updated = current.includes(value)
        ? current.filter(v => v !== value)
        : [...current, value];
      return { ...prev, [questionId]: updated };
    });
    console.log(answers);
  };

  const handleSubmit = async () => {
    const res = await fetch('/api/questions', {
      method: 'POST',
      body: JSON.stringify({
        answers: answers,
      }),
    });
    console.log(res);
    if (res.ok) {
      router.push('/job-match');
    } else {
      console.error('Failed to submit questionnaire');
    }
  };

  const shouldShowQuestion = (question: Question): boolean => {
    if (!question.showCondition) return true;

    const { questionId, selectedValue } = question.showCondition;
    return answers[questionId] === selectedValue;
  };

  return (
    <div className='space-y-6'>
      {questions.filter(shouldShowQuestion).map((question: Question) => (
        <div key={question.id} className='p-4 border rounded-lg'>
          <h3 className='text-lg font-medium mb-4'>{question.label}</h3>

          <div className='space-y-2'>
            {question.options.map(option => (
              <button
                type='button'
                key={option}
                onClick={() => {
                  if (question.type === 'multi') {
                    handleMultiChoice(question.id, option);
                  } else {
                    handleSingleChoice(question.id, option);
                  }
                }}
                className={`
                  w-full p-3 text-left border rounded-md transition-colors
                  ${
                    question.type === 'multi'
                      ? (answers[question.id] as string[])?.includes(option)
                        ? 'bg-blue-100 border-blue-500'
                        : 'bg-white border-gray-300 hover:bg-gray-50'
                      : answers[question.id] === option
                        ? 'bg-blue-100 border-blue-500'
                        : 'bg-white border-gray-300 hover:bg-gray-50'
                  }
                `}
              >
                {option}
              </button>
            ))}
          </div>
        </div>
      ))}

      <div className='mt-8 text-center'>
        <button type='submit' onClick={handleSubmit}>
          求人マッチングを開始
        </button>
      </div>
    </div>
  );
};
