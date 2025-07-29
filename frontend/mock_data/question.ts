import type { Question } from '@/types/question';

export const questions: Question[] = [
  {
    id: '1',
    type: 'choice',
    label: '希望職種を選んでください',
    options: ['イベント', '飲食', '接客', '医療・福祉'],
  },
  {
    id: '2',
    type: 'choice',
    label: '過去にアルバイト経験はありますか？',
    options: ['はい', 'いいえ'],
  },
  {
    id: '3',
    type: 'multi',
    label: '過去に経験のある職種を選んでください',
    options: ['イベント', '飲食', '接客'],
    showCondition: { questionId: 2, selectedValue: 'はい' },
  },
  {
    id: '4',
    type: 'choice',
    label: '求人情報の推薦に、過去に経験のある職種を含めますか？',
    options: ['はい', 'いいえ'],
    showCondition: { questionId: 2, selectedValue: 'はい' },
  },
  {
    id: '5',
    type: 'coice',
    label: '求人情報の推薦に、同じ業種の求人情報を含めますか？',
    options: ['はい', 'いいえ'],
    showCondition: { questionId: 2, selectedValue: 'はい' },
  },
];

//     "workValueOptions": [
//     "安定した収入",
//     "柔軟な勤務時間",
//     "新しいスキル習得",
//     "人との交流",
//     "責任のある仕事",
//     "創造性を活かす",
//     "高い給与",
//     "将来への投資"
//   ],
//   "jobCategoryOptions": [
//     "飲食・レストラン",
//     "販売・接客",
//     "オフィスワーク",
//     "教育・指導",
//     "イベント・エンタメ",
//     "配達・運送",
//     "クリエイティブ",
//     "その他"
//   ],
//   "experienceOptions": [
//     "飲食業",
//     "小売業",
//     "オフィスワーク",
//     "教育・指導",
//     "イベントスタッフ",
//     "配達・運送",
//     "クリエイティブ業界",
//     "なし"
//   ],
//   "locationOptions": [
//     "渋谷区",
//     "新宿区",
//     "池袋区",
//     "品川区",
//     "世田谷区",
//     "中央区",
//     "港区",
//     "リモート可",
//     "その他"
//   ]
// }
