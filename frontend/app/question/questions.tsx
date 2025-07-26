import type { Question } from '@/types/question';

type Props = {
  questions: Question[];
};

export const Questions = ({ questions }: Props) => {
  return (
    <div>
      {questions.map((question: Question) => (
        <div key={question.id}></div>
      ))}
    </div>
  );
};
