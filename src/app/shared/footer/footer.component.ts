import { Component } from '@angular/core';
import { FormControl } from '@angular/forms';

declare const $: any;

@Component({
  selector: 'app-footer-cmp',
  templateUrl: 'footer.component.html',
  styleUrls: ['./footer.component.css'],
})
export class FooterComponent {
  test: Date = new Date();
  user_deatail = localStorage.getItem('livis_user');
  isBotActive = false;

  inputQts = new FormControl();
  messages = [
    {
      type: 'ans',
      res:
        "Hi there 🖐. I’m your virtual assistant. I'm here to help with your general enquiries.",
    },
  ];
  imageSrc = '';
  options: string[] = [];
  year: number;
  // options: string[] = [
  //   'How do I set up a new camera on my existing workstation? Is it possible to use my phone camera for inspection?',
  //   'Is it possible to add more data and train the same part again?',
  //   'Show me a sample Inference image for the PCBA_OP4830 part. What is the current accuracy on this part?',
  //   'Show me the annotated data distribution chart for L shaped part',
  // ];

  // public feed: Observable<Message[]>;

  // public readonly user: User = {
  //   id: 1,
  // };

  // public readonly bot: User = {
  //   id: 0,
  // };

  // private local: Subject<Message> = new Subject<Message>();

  // constructor(private svc: ChatService) {
  //   const hello: Message = {
  //     author: this.bot,
  //     suggestedActions: [
  //       {
  //         type: 'reply',
  //         value:
  //           'How do I set up a new camera on my existing workstation? Is it possible to use my phone camera for inspection?',
  //       },
  //       {
  //         type: 'reply',
  //         value:
  //           'Is it possible to add more data and train the same part again?',
  //       },
  //     ],
  //     timestamp: new Date(),
  //     text: 'Hello, how can I help you?',
  //   };

  //   // Merge local and remote messages into a single stream
  //   this.feed = merge(
  //     from([hello]),
  //     this.local,
  //     this.svc.responses.pipe(
  //       map(
  //         (response): Message => ({
  //           author: this.bot,
  //           text: response,
  //         })
  //       )
  //     )
  //   ).pipe(
  //     // ... and emit an array of all messages
  //     scan((acc: Message[], x: Message) => [...acc, x], [])
  //   );
  // }
  ngOnInit() {
    var date = new Date();
    this.year = date.getFullYear();
  }
  public showBot(): void {
    this.isBotActive = true;
  }

  public closeBot(): void {
    this.isBotActive = false;
  }

  changeQts(e) {
    this.inputQts = e.target.value;
  }

  qtsInput(e) {
    const value = e.target.value;
    if (value.length > 2) {
      //console.log(`HERE: ${value.length}`);
      const options = [
        'How do I set up a new camera on my existing workstation? Is it possible to use my phone camera for inspection?',
        'Is it possible to add more data and train the same part again?',
        'Show me a sample Inference image for the PCBA_OP4830 part. What is the current accuracy on this part?',
        'Show me the annotated data distribution chart for L shaped part',
      ];
      this.options = [];
      for (const option of options) {
        if (
          option.toLowerCase().includes(value.toLowerCase()) &&
          !this.options.includes(option)
        ) {
          this.options.push(option);
        }
      }
    } else {
      this.options = [];
    }
  }

  submitMsg(): void {
    //console.log(this.inputQts);
    this.messages.push({
      type: 'qts',
      res: this.inputQts.value,
    });
    setTimeout(() => {
      this.adjustScroll();
    }, 100);

    let ans =
      'Sorry, we are unable to answer your query. Feel free to call our support team directly at +1 407 837 6852.';
    let type = 'ans';

    if (
      this.inputQts.value.includes(
        'set up a new camera on my existing workstation'
      )
    ) {
      type = 'qts1';
      ans = `To set up a new camera follow the steps below:
      a. Login as an Admin
      b. Click on Configuration icon
      c. On the left side panel, click on Config
      d. Select Workstations from the dropdown menu
      e. For a specific workstation, click on the pencil icon
      f.  In the edit menu click on add another camera
      g. Specify the camera name and its Id
      h. Click on Submit button

      Yes, it is possible to use phone camera, make sure to connect to the same network and add camera rtsp stream ip address in place of camera id while configuring workstation camera`;
    }

    if (
      this.inputQts.value.includes(
        'possible to add more data and train the same part again'
      )
    ) {
      type = 'qts2';
      ans = `Yes, it is possible to add more data to an already trained part to train it again.
      Follow the below procedure to add more data

      a. Login as Admin
      b. Click on Capture
      c. Select the workstation and part in the dropdown
      d. Click on add data
      e. We can either capture more data using the camera or we can upload a zip file containing images
      f. Annotate the newly added images
      g. Follow the usual training procedure to train the part
      h. New version would be added after the training is successful with better accuracy which would be ready for deployment`;
    }

    if (this.inputQts.value.includes('PCBA_OP4830')) {
      type = 'image';
      ans = `../../../assets/frame.jpg`;
      this.imageSrc = ans;
    }

    if (
      this.inputQts.value.includes(
        'annotated data distribution chart for L shaped part'
      )
    ) {
      type = 'image';
      ans = `../../../assets/graph.jpg`;
      this.imageSrc = ans;
    }

    this.inputQts.setValue('');
    setTimeout(() => {
      this.messages.push({
        type: type,
        res: ans,
      });
      setTimeout(() => {
        this.adjustScroll();
      }, 100);
    }, 1000);
  }

  openImageModal() {
    $('#image-modal').modal('show');
  }

  adjustScroll() {
    const messageArea = document.querySelector('.chatbot__message-window');
    if (messageArea) {
      messageArea.scrollTop = messageArea.scrollHeight;
    }
  }

  // public sendMessage(e: SendMessageEvent): void {
  //   this.local.next(e.message);

  //   this.local.next({
  //     author: this.bot,
  //     typing: true,
  //   });

  //   if (e.message.text.includes('workstation')) {
  //     this.svc.first(e.message.text);
  //   }
  //   if (e.message.text.includes('part again')) {
  //     this.svc.second(e.message.text);
  //   }
  // }
}
