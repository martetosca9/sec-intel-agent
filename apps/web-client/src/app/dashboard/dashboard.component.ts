import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatMenuModule } from '@angular/material/menu';
import { ThreatApiService } from '../threat-api.service';
import { LanguageService } from '../language.service';
import { NewsItem, AnalysisResult } from '../models';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatToolbarModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatCardModule,
    MatIconModule,
    MatProgressBarModule,
    MatSnackBarModule,
    MatMenuModule
  ],
  template: `
    <mat-toolbar color="primary">
      <span>{{ ls.t.title }}</span>
      <span class="spacer"></span>
      
      <button mat-button [matMenuTriggerFor]="menu" class="lang-btn">
        <mat-icon>language</mat-icon>
        {{ ls.lang === 'en' ? 'English' : 'Español' }}
      </button>
      <mat-menu #menu="matMenu">
        <button mat-menu-item (click)="ls.toggleLanguage()">
          {{ ls.lang === 'en' ? 'Cambiar a Español' : 'Switch to English' }}
        </button>
      </mat-menu>

      <button mat-flat-button color="accent" (click)="onIngest()" [disabled]="loading">
        <mat-icon>refresh</mat-icon> {{ ls.t.refreshBtn }}
      </button>
    </mat-toolbar>

    <div class="container">
      <div class="search-section">
        <mat-form-field appearance="outline" class="search-field">
          <mat-label>{{ ls.t.searchPlaceholder }}</mat-label>
          <input matInput [(ngModel)]="searchQuery" (keyup.enter)="onSearch()" [disabled]="loading">
          <button mat-icon-button matSuffix (click)="onSearch()" [disabled]="loading">
            <mat-icon>search</mat-icon>
          </button>
        </mat-form-field>
        
        <button mat-raised-button color="primary" class="analyze-btn" 
                (click)="onAnalyze()" [disabled]="loading || !searchQuery">
          <mat-icon>psychology</mat-icon> {{ ls.t.analyzeBtn }}
        </button>
      </div>

      <mat-progress-bar mode="indeterminate" *ngIf="loading"></mat-progress-bar>

      <div class="main-content">
        <!-- Analysis Panel -->
        <mat-card class="analysis-card" *ngIf="analysis">
          <mat-card-header>
            <mat-card-title>{{ ls.t.analysisTitle }}</mat-card-title>
            <mat-card-subtitle>{{ ls.t.analysisSubtitle }}</mat-card-subtitle>
          </mat-card-header>
          <mat-card-content>
            <p class="analysis-text">{{ analysis.analysis }}</p>
            <div class="sources">
              <strong>{{ ls.t.sourcesTitle }}</strong>
              <ul>
                <li *ngFor="let source of analysis.sources">
                  <a [href]="source" target="_blank">{{ source }}</a>
                </li>
              </ul>
            </div>
          </mat-card-content>
        </mat-card>

        <!-- News Results -->
        <div class="news-grid">
          <mat-card class="news-card" *ngFor="let item of news">
            <mat-card-header>
              <mat-card-title>{{ item.title }}</mat-card-title>
              <mat-card-subtitle>{{ item.source }}</mat-card-subtitle>
            </mat-card-header>
            <mat-card-content>
              <p>{{ item.summary }}</p>
            </mat-card-content>
            <mat-card-actions>
              <a mat-button color="primary" [href]="item.source" target="_blank">{{ ls.t.readMore }}</a>
            </mat-card-actions>
          </mat-card>
        </div>

        <div class="empty-state" *ngIf="!loading && news.length === 0 && !analysis">
          <mat-icon>search_off</mat-icon>
          <p>{{ ls.t.emptyState }}</p>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .spacer { flex: 1 1 auto; }
    .container { padding: 20px; max-width: 1200px; margin: 0 auto; }
    .search-section { display: flex; gap: 10px; align-items: center; margin-bottom: 20px; }
    .search-field { flex: 1; }
    .analyze-btn { height: 56px; margin-bottom: 22px; }
    .lang-btn { margin-right: 15px; }
    
    .main-content { margin-top: 20px; }
    
    .analysis-card { margin-bottom: 30px; border-left: 5px solid #ff4081; background-color: #fffafb; }
    .analysis-text { white-space: pre-wrap; line-height: 1.6; font-size: 1.1rem; }
    .sources { margin-top: 15px; font-size: 0.9rem; }
    
    .news-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 20px; }
    .news-card { display: flex; flex-direction: column; justify-content: space-between; }
    
    .empty-state { text-align: center; margin-top: 100px; color: #666; }
    .empty-state mat-icon { font-size: 48px; width: 48px; height: 48px; margin-bottom: 10px; }
  `]
})
export class DashboardComponent implements OnInit {
  searchQuery: string = '';
  news: NewsItem[] = [];
  analysis: AnalysisResult | null = null;
  loading: boolean = false;

  constructor(
    private apiService: ThreatApiService,
    public ls: LanguageService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    // Optionally load initial news
    this.searchQuery = 'latest';
    this.onSearch();
  }

  onSearch(): void {
    if (!this.searchQuery) return;
    this.loading = true;
    this.analysis = null;
    this.apiService.search(this.searchQuery).subscribe({
      next: (results) => {
        this.news = results;
        this.loading = false;
      },
      error: (err) => {
        this.showError(this.ls.t.errorSearch);
        this.loading = false;
      }
    });
  }

  onAnalyze(): void {
    if (!this.searchQuery) return;
    this.loading = true;
    this.apiService.analyze(this.searchQuery).subscribe({
      next: (result) => {
        this.analysis = result;
        this.loading = false;
      },
      error: (err) => {
        this.showError(this.ls.t.errorAnalyze);
        this.loading = false;
      }
    });
  }

  onIngest(): void {
    this.loading = true;
    this.apiService.ingest().subscribe({
      next: (resp) => {
        this.snackBar.open(resp.message, this.ls.t.close, { duration: 3000 });
        this.onSearch(); // Refresh with current query
      },
      error: (err) => {
        this.showError(this.ls.t.errorIngest);
        this.loading = false;
      }
    });
  }

  private showError(msg: string): void {
    this.snackBar.open(msg, this.ls.t.close, { duration: 5000, panelClass: ['error-snackbar'] });
  }
}
