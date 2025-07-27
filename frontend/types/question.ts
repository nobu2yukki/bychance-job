export type Question = {
  //id: number;
  id: string;
  type: string;
  label: string;
  options: string[];
  showCondition?: {
    questionId: number;
    selectedValue: string;
  };
};
