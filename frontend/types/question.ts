export type Question = {
  id: number;
  type: string;
  label: string;
  options: string[];
  showCondition?: {
    questionId: number;
    selectedValue: string;
  };
};
