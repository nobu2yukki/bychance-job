import { questions } from '@/mock_data/question';
import { useEffect } from 'react';
import { Questions } from './questions';

export default function Home() {
  useEffect(() => {
    // TODO: fetch処理
  }, []);

  return (
    <main>
      <h1>アンケート画面</h1>
      <p>Q1.希望する職種は？</p>
      <Questions questions={questions} />
    </main>
  );
}
