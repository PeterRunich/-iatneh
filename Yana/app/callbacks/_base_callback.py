class BaseCallback:
    async def handle(self, cq, callback_answer=True):
        self.callback_id, self.action, *self.args = cq.data.split(':')
        self.message_id = cq['message']['message_id']
        self.chat_id = cq['message']['chat']['id']
        self.message_text = cq['message']['text']
        self.callback_answer = callback_answer
        self.cq = cq

        if self.args == ['']: self.args = []
        
        await self._call()

    async def _call(self):
        if not hasattr(self, self.action): self._method_missing(); return;

        await getattr(self, self.action)(*self.args)

        if self.callback_answer: await self.cq.answer()

    def _method_missing(self):
        raise RuntimeError(f'action: {self.action} не был реализован для callback_id: {self.callback_id} в классе: {self.__class__.__name__}')

    async def no_action(self):
        pass
