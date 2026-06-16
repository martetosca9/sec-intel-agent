import { Injectable, signal } from '@angular/core';

export type Language = 'en' | 'es';

@Injectable({
  providedIn: 'root'
})
export class LanguageService {
  private currentLang = signal<Language>('es');

  translations = {
    en: {
      title: 'CyberThreat Intelligence Hub',
      refreshBtn: 'Refresh News',
      searchPlaceholder: 'Search threats or news...',
      analyzeBtn: 'AI Analysis (Llama 3)',
      analysisTitle: 'Intelligence Analysis',
      analysisSubtitle: 'AI generated based on current results',
      sourcesTitle: 'Sources consulted:',
      readMore: 'READ MORE',
      emptyState: 'No news to display. Try searching or updating the database.',
      close: 'Close',
      errorSearch: 'Error searching news',
      errorAnalyze: 'Error generating analysis. Is Ollama running?',
      errorIngest: 'Error updating news'
    },
    es: {
      title: 'Centro de Inteligencia de Ciberamenazas',
      refreshBtn: 'Actualizar Noticias',
      searchPlaceholder: 'Buscar amenazas o noticias...',
      analyzeBtn: 'Análisis IA (Llama 3)',
      analysisTitle: 'Análisis de Inteligencia',
      analysisSubtitle: 'Generado por IA en base a resultados actuales',
      sourcesTitle: 'Fuentes consultadas:',
      readMore: 'LEER MÁS',
      emptyState: 'No hay noticias para mostrar. Intenta buscar algo o actualizar la base de datos.',
      close: 'Cerrar',
      errorSearch: 'Error al buscar noticias',
      errorAnalyze: 'Error al generar el análisis. ¿Está Ollama corriendo?',
      errorIngest: 'Error al actualizar las noticias'
    }
  };

  get lang() {
    return this.currentLang();
  }

  get t() {
    return this.translations[this.currentLang()];
  }

  toggleLanguage() {
    this.currentLang.set(this.currentLang() === 'en' ? 'es' : 'en');
  }
}
