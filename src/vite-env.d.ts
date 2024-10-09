/// <reference types="vite/client" />

import router from './router/router';

declare module '*.vue' {
  import { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

declare module 'tailwindcss' {
    const tailwind: any;
    export default tailwind;
  }
  
  declare module 'autoprefixer' {
    const autoprefixer: any;
    export default autoprefixer;
  }
  
  declare module 'dotenv' {
    interface DotenvConfigOptions {
      path?: string;
      encoding?: string;
      debug?: boolean;
    }
  
    interface DotenvParseOutput {
      [name: string]: string;
    }
  
    interface DotenvConfigOutput {
      parsed?: DotenvParseOutput;
      error?: Error;
    }
  
    function config(options?: DotenvConfigOptions): DotenvConfigOutput;
    function parse(src: string | Buffer): DotenvParseOutput;
  
    export { config, parse, DotenvConfigOptions, DotenvParseOutput, DotenvConfigOutput };
  }
  declare module router {
    const router: any;
    export default router;
  }
