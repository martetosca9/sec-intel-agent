export interface NewsItem {
  title: string;
  source: string;
  summary: string;
}

export interface SearchQuery {
  query: string;
  k?: number;
}

export interface AnalysisResult {
  analysis: string;
  sources: string[];
}
