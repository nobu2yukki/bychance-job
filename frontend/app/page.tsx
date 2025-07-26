import Link from "next/link";

export default function Home() {
  return (
    <main>
      <div className="flex flex-col items-center h-screen">
        <h1 className="text-red-400 text-5xl">byChance-job</h1>
        <p className="text-4xl">直感的にアルバイト求人を探そう！</p>
        <Link href="question">
          <button className="goQuestion" type="button">アンケート画面へ</button>
        </Link>
      </div>
    </main>
  );
}
