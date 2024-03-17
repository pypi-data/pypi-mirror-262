import discord.errors
from discord.ui import View
from discord import ButtonStyle
from typing import Union


class Faginator(View):
    def __init__(self, ctx, embeds: list = None, content: list = None, extra_buttons: list = None,
                 delete_on_timeout: bool = False, disable_on_timeout: bool = True, timeout: Union[int, None] = 180,
                 close_button: bool = True, show_pages: bool = True, only_author: bool = True,
                 select_menu: list = None, lang: str = 'en'):

        super().__init__(timeout=timeout)

        self.disable_on_timeout = disable_on_timeout
        self.ctx = ctx
        self.cur_page = 0

        if extra_buttons is not None and extra_buttons != []:
            for _ in range(len(extra_buttons)):
                extra_buttons[_] = extra_buttons[_][:5]
                for u in range(len(extra_buttons[_])):
                    extra_buttons[_][u].row = 0
            for _ in extra_buttons[self.cur_page]: self.add_item(_)

        self.extra_buttons = extra_buttons
        self.delete_on_timeout = delete_on_timeout
        self.only_author = only_author
        self.select_menu = select_menu

        if show_pages:
            if embeds is not None:
                self.embeds = [
                    embeds[i].set_footer(text=f'{"Page" if lang == "en" else "Страница"} {i + 1}/{len(embeds)}') for i
                    in range(len(embeds))]
            if content is not None and embeds is None:
                self.content = [content[i] + f'\n\n{"Page" if lang == "en" else "Страница"} {i + 1}/{len(content)}' for
                                i in range(len(content))]
            elif content is not None:
                self.content = content
            if content is None:
                self.content = None
            if embeds is None:
                self.embeds = None

        else:
            if embeds is not None:
                self.embeds = embeds
            if content is not None:
                self.content = content

            if content is None:
                self.content = None
            if embeds is None:
                self.embeds = None

        deter_button = [_ for _ in self.children if _.custom_id == 'close_button'][0]
        back_button = [_ for _ in self.children if _.custom_id == 'previous_button'][0]
        next_button = [_ for _ in self.children if _.custom_id == 'next_button'][0]

        self.deter_button = deter_button
        self.back_button = back_button
        self.next_button = next_button
        self.close_button = close_button

        if not close_button:
            self.remove_item(deter_button)

        if self.select_menu is not None and len(self.select_menu) == 1:
            self.add_item(self.select_menu[0])
        elif self.select_menu is not None and len(self.select_menu) != 1:
            self.add_item(self.select_menu[0])

        if (self.embeds is not None and len(self.embeds) == 1) or (self.content is not None and len(self.content) == 1):
            next_button.disabled = True
            back_button.disabled = True

        back_button.disabled = True

    def check_emb_content_view(self) -> list:
        if self.content is not None:
            new_content = self.content[self.cur_page]
        else:
            new_content = None
        if self.embeds is not None:
            new_emb = self.embeds[self.cur_page]
        else:
            new_emb = None
        return [new_emb, new_content]

    async def interaction_check(self, interaction) -> bool:
        try:
            return ((interaction.user == self.ctx.author) if self.only_author else True)
        except:
            return ((interaction.user == self.ctx.user) if self.only_author else True)

    async def on_timeout(self) -> None:
        if bool(self.parent):
            if self.disable_on_timeout:
                try:
                    self.disable_all_items()
                    await self.parent.edit_original_response(view=self)
                except Exception as e:
                    print(e)
            if self.delete_on_timeout:
                try:
                    await self.parent.delete_original_response()
                except Exception as e:
                    print(e)
        elif bool(self.message):
            if self.disable_on_timeout:
                try:
                    self.disable_all_items()
                    await self.parent.edit_original_response(view=self)
                except Exception as e:
                    print(e)
            if self.delete_on_timeout:
                try:
                    await self.parent.delete_original_response()
                except Exception as e:
                    print(e)
        try:
            self.stop()
        except Exception as e:
            print(e)

    async def disable(self, remove_buttons: bool = False, remove_message: bool = False, disable_buttons: bool = True):
        if remove_buttons:
            self.clear_items()
            if bool(self.parent):
                await self.parent.edit_original_response(view=self)
            elif bool(self.message):
                await self.message.edit(view=self)
        if remove_message:
            if bool(self.parent):
                await self.parent.delete_original_response()
            elif bool(self.message):
                await self.message.delete()
        if disable_buttons:
            self.disable_all_items()
            if bool(self.parent):
                await self.parent.edit_original_response(view=self)
            elif bool(self.message):
                await self.message.edit(view=self)
        self.stop()

    @discord.ui.button(style=ButtonStyle.secondary, row=1, emoji='◀️',
                       custom_id="previous_button")
    async def back_callback(self, button, interaction):
        self.next_button.disabled = False
        self.cur_page -= 1
        if self.cur_page == 0:
            button.disabled = True
        else:
            button.disabled = False

        self.clear_items()
        if self.extra_buttons is not None:
            for _ in self.extra_buttons[self.cur_page]: self.add_item(_)
            [self.add_item(i) for i in [self.back_button, self.next_button]]
            if self.close_button: self.add_item(self.deter_button)
        else:
            [self.add_item(i) for i in [self.back_button, self.next_button]]
            if self.close_button: self.add_item(self.deter_button)

        if self.select_menu is not None and len(self.select_menu) == 1:
            self.add_item(self.select_menu[0])
        elif self.select_menu is not None and len(self.select_menu) != 1:
            self.add_item(self.select_menu[self.cur_page])

        new_emb, new_cont = self.check_emb_content_view()
        await interaction.response.edit_message(embed=new_emb, content=new_cont, view=self)

    @discord.ui.button(style=ButtonStyle.secondary, row=1, emoji="▶️", custom_id="next_button")
    async def next_callback(self, button, interaction):
        self.back_button.disabled = False
        self.cur_page += 1

        if self.embeds is not None:
            if (self.cur_page + 1 == len(self.embeds)):
                button.disabled = True
            else:
                button.disabled = False
        elif self.content is not None:
            if (self.cur_page + 1 == len(self.content)):
                button.disabled = True
            else:
                button.disabled = False

        self.clear_items()
        if self.extra_buttons is not None:
            for _ in self.extra_buttons[self.cur_page]: self.add_item(_)
            [self.add_item(i) for i in [self.back_button, self.next_button]]
            if self.close_button: self.add_item(self.deter_button)
        else:
            [self.add_item(i) for i in [self.back_button, self.next_button]]
            if self.close_button: self.add_item(self.deter_button)

        if self.select_menu is not None and len(self.select_menu) == 1:
            self.add_item(self.select_menu[0])
        elif self.select_menu is not None and len(self.select_menu) != 1:
            self.add_item(self.select_menu[self.cur_page])

        new_emb, new_cont = self.check_emb_content_view()
        await interaction.response.edit_message(embed=new_emb, content=new_cont, view=self)


    @discord.ui.button(style=ButtonStyle.red, row=1, emoji='🛑', custom_id="close_button")
    async def close_callback(self, button, interaction):
        try:
            await self.message.delete()
            self.stop()
        except discord.errors.NotFound:
            print("[ERROR] Seems like your message ephemeral or posted before latest bot restart")
        except Exception as e:
            raise e

    async def start(self, interact: discord.Interaction = None, ephemeral: bool = False, type: str = 'slash', action: str = 'send'):
        new_emb, new_cont = self.check_emb_content_view()

        if type == 'slash':
            await self.ctx.respond(view=self, embed=new_emb, content=new_cont, ephemeral=ephemeral)
        elif type == 'interaction':
            if action == 'send':
                await interact.response.send_message(view=self, embed=new_emb, content=new_cont, ephemeral=ephemeral)
            else:
                await interact.response.edit_message(view=self, embed=new_emb, content=new_cont)

    async def on_error(self, error, item, interaction):
        raise error
