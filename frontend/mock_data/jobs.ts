import type { Job } from '@/types/jobs';

export const sampleJobs: Job[] = [
  {
    id: 1,
    company_name: 'スターバックス 渋谷店',
    description:
      'お客様への接客、コーヒーの提供、レジ操作などをお任せします。未経験の方も歓迎！充実した研修制度があります。明るく笑顔で接客できる方を募集しています。',
    salary: '1200-1400円/時',
    place: '渋谷区',
    category: {
      parent: '飲食・レストラン',
      child: 'カフェスタッフ',
    },
    image_url: 'https://images.unsplash.com/photo-1442512595331-e89e73853f31?w=500&h=300&fit=crop',
    work_style: ['交通費支給', '制服貸与', '社員割引', '研修充実', '昇給あり'],
    audience: ['大学生', '社会人', '未経験歓迎'],
  },
  {
    id: 2,
    company_name: 'UNIQLO 新宿店',
    description:
      'お客様への接客販売、商品整理、レジ業務をお願いします。ファッションが好きな方大歓迎！最新のトレンドを学びながら働けます。',
    salary: '1300-1500円/時',
    place: '新宿区',
    category: {
      parent: '販売・接客',
      child: 'アパレル販売員',
    },
    image_url: 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=500&h=300&fit=crop',
    work_style: [
      '接客経験者優遇',
      '土日勤務可能',
      '大学生歓迎',
      'ファッションに興味がある方',
    ],
    audience: ['大学生', '社会人', '未経験歓迎'],
  },
  {
    id: 3,
    company_name: '株式会社テックソリューション',
    description:
      '簡単なデータ入力作業をお任せします。在宅勤務可能で、自分のペースで作業できます。Excel等の基本操作ができれば問題ありません。',
    salary: '1100-1200円/時',
    place: 'リモート可',
    category: {
      parent: 'オフィスワーク',
      child: 'データ入力',
    },
    image_url: 'https://images.unsplash.com/photo-1556761175-b413da4baf72?w=500&h=300&fit=crop',
    work_style: [
      '基本的なPC操作ができる',
      '責任感を持って作業できる',
      '学生歓迎',
      'Excel基本操作',
    ],
    audience: ['大学生', '社会人', '未経験歓迎'],
  },
  {
    id: 4,
    company_name: '個別指導塾ITTO',
    description:
      '小中高生への個別指導をお任せします。教える科目は相談可能。教育に興味のある方歓迎！生徒の成長を間近で感じられるやりがいのある仕事です。',
    salary: '1500-2000円/時',
    place: '池袋区',
    category: {
      parent: '教育・指導',
      child: '個別指導塾講師',
    },
    image_url: 'https://images.unsplash.com/photo-1509062522246-3755977927d7?w=500&h=300&fit=crop',
    work_style: [
      '大学生以上',
      '得意科目がある',
      '週2日以上勤務可能',
      '教育に興味がある方',
    ],
    audience: ['大学生', '社会人', '未経験歓迎'],
  },
  {
    id: 5,
    company_name: 'イベントプロダクション',
    description:
      'コンサートやイベントの会場設営、案内業務をお願いします。単発から長期まで選べます。有名アーティストのイベントにも関われます！',
    salary: '1200-1500円/時',
    place: '都内各所',
    category: {
      parent: 'イベント・エンタメ',
      child: 'イベントスタッフ',
    },
    image_url: 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=500&h=300&fit=crop',
    work_style: [
      '体力に自信がある',
      '土日勤務可能',
      '協調性がある',
      '立ち仕事OK',
    ],
    audience: ['大学生', '社会人', '未経験歓迎'],
  },
  {
    id: 6,
    company_name: 'Uber Eats',
    description:
      '自転車やバイクを使ったフードデリバリーのお仕事です。完全に自分のペースで働けて、頑張った分だけ稼げます！',
    salary: '1000-1800円/時',
    place: '東京都内',
    category: {
      parent: '配達・運送',
      child: 'デリバリースタッフ',
    },
    image_url: 'https://images.unsplash.com/photo-1565793298595-6a879b1d9492?w=500&h=300&fit=crop',
    work_style: [
      '18歳以上',
      '自転車またはバイク所有',
      '体力に自信がある',
      'スマホ操作可能',
    ],
    audience: ['大学生', '社会人', '未経験歓迎'],
  },
  {
    id: 7,
    company_name: 'セブンイレブン 新宿西口店',
    description:
      'レジ業務、商品陳列、清掃等のコンビニ業務全般をお願いします。深夜帯は時給アップ！未経験でも丁寧に指導します。',
    salary: '1050-1350円/時',
    place: '新宿区',
    category: {
      parent: '販売・接客',
      child: 'コンビニスタッフ',
    },
    image_url: 'https://images.unsplash.com/photo-1555487505-50e21e4b2cd1?w=500&h=300&fit=crop',
    work_style: [
      '高校生OK',
      '深夜勤務できる方歓迎',
      '週3日以上勤務可能',
      '未経験歓迎',
    ],
    audience: ['大学生', '社会人', '未経験歓迎'],
  },
  {
    id: 8,
    company_name: 'クリエイティブスタジオ',
    description:
      'Webデザインのアシスタント業務をお任せします。Photoshop、Illustratorが使える方歓迎。実務経験を積みたい学生にもおすすめです。',
    salary: '1300-1600円/時',
    place: '渋谷区',
    category: {
      parent: 'オフィスワーク',
      child: 'Webデザインアシスタント',
    },
    image_url: 'https://images.unsplash.com/photo-1517180102446-f3ece451e9d8?w=500&h=300&fit=crop',
    work_style: [
      'Photoshop, Illustrator使用経験',
      '大学生・専門学生歓迎',
      'デザインに興味がある方',
      '平日勤務可能',
    ],
    audience: ['大学生', '社会人', '未経験歓迎'],
  },
  {
    id: 9,
    company_name: 'ペットランド',
    description:
      '可愛いペットたちのお世話と接客業務をお願いします。動物好きにはたまらないお仕事！ペットとの触れ合いで癒されながら働けます。',
    salary: '1100-1300円/時',
    place: '世田谷区',
    category: {
      parent: '販売・接客',
      child: 'ペットショップスタッフ',
    },
    image_url: 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=500&h=300&fit=crop',
    work_style: [
      '動物好き必須',
      '責任感がある方',
      '土日勤務可能',
      '高校生OK',
    ],
    audience: ['大学生', '社会人', '未経験歓迎'],
  },
  {
    id: 10,
    company_name: 'ドミノピザ　浜松西伊場店',
    description:
      '新作ゲームのテストプレイとバグ報告をお願いします。ゲーム好きにはたまらないお仕事！リリース前のゲームを一足先に体験できます。',
    salary: '1200-1400円/時',
    place: '品川区',
    category: {
      parent: 'オフィスワーク',
      child: 'ゲームテスター',
    },
    image_url: 'https://images.unsplash.com/photo-1493711662062-fa541adb3fc8?w=500&h=300&fit=crop',
    work_style: [
      'ゲーム好き',
      '集中力がある方',
      '細かい作業が得意',
      '平日勤務可能',
    ],
    audience: ['大学生', '社会人', '未経験歓迎'],
  },
];
