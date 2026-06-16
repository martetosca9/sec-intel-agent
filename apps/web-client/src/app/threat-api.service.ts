import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { NewsItem, SearchQuery, AnalysisResult } from './models';

@Injectable({
  providedIn: 'root'
})
export class ThreatApiService {
  constructor(private http: HttpClient) {}

  ingest(): Observable<{ status: string; message: string }> {
    return this.http.post<{ status: string; message: string }>('/ingest', {});
  }

  search(query: string, k: number = 5): Observable<NewsItem[]> {
    return this.http.post<NewsItem[]>('/search', { query, k });
  }

  analyze(query: string): Observable<AnalysisResult> {
    return this.http.post<AnalysisResult>('/analyze', { query });
  }
}
