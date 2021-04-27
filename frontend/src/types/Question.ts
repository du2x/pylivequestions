export interface Question {
    text: string
    options: QOption[]    
    type: string
    uuid: string
  }
  
  export interface QOption {
      ref: string
      text: string
  }

  export interface FQuestion {
    text: string
    options: FQOption[]    
    type: string
    uuid: string
    pickedAt: any
  }
  
  export interface FQOption {
      correct: boolean
      text: string
      post_text: string      
  }

  