import Link from 'next/link';

export default function Home() {
  return (
    <main className='px-5'>
      <div className='flex flex-col items-center justify-center h-screen'>
        <h1 className='text-5xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight'>
          ByChanceJob
        </h1>
        <p className='text-xl text-gray-600 mb-12 max-w-2xl mx-auto leading-relaxed'>
          直感的な操作で、あなたにぴったりの
          <br />
          アルバイトを発見
          <br />
          右スワイプで気になる求人とあなたを
          <br />
          マッチング！
        </p>
        <Link href='question'>
          <button
            className='bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white font-bold py-4 px-12 rounded-full text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300 hover:scale-105'
            type='button'
          >
            アンケートに答える
          </button>
        </Link>
      </div>
    </main>
  );
}
