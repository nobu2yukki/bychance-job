'use client';

import { useState } from 'react';
import Link from 'next/link';
import type { Question } from '@/types/question';

type Props = {
  questions: Question[];
};

export const Questions = ({ questions }: Props) => {
  const [answers, setAnswers] = useState<Record<number, string | string[]>>({});

  const handleSingleChoice = (questionId: number, value: string) => {
    setAnswers(prev => ({ ...prev, [questionId]: value }));
  };

  const handleMultiChoice = (questionId: number, value: string) => {
    setAnswers(prev => {
      const current = (prev[questionId] as string[]) || [];
      const updated = current.includes(value)
        ? current.filter(v => v !== value)
        : [...current, value];
      return { ...prev, [questionId]: updated };
    });
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
        <Link 
          href='/job-match'
          className='inline-block px-6 py-3 bg-blue-500 text-white font-medium rounded-md hover:bg-blue-600 transition-colors'
        >
          求人マッチングを開始
        </Link>
      </div>
    </div>
  );
};
