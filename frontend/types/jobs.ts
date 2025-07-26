export type Job = {
  id: number;
  company_name: string;
  page_url: string;
  image_url: string;
  place: string;
  salary: string;
  description: string;
  category: {
    parent: string;
    child: string;
  }
  work_style: string[];
  audience: string[];
}

