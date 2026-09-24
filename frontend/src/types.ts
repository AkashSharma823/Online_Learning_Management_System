export type Role = "student" | "instructor" | "admin";
export interface User { id:number; username:string; first_name:string; last_name:string; email:string; role:Role; }
export interface Course { id:number; title:string; slug:string; description:string; price:number; level:string; duration:string; thumbnail:string; instructor_name?:string; category_name?:string; }
export interface TableRow { [key:string]: string|number|boolean|undefined }
